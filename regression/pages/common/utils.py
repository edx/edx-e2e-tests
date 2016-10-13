# -*- coding: utf-8 -*-

"""
Different utilities to be used in tests
"""
import re
import time
import functools
import datetime
import imaplib
import email

import requests
from requests.auth import HTTPBasicAuth
from edx_rest_api_client.client import EdxRestApiClient
from opaque_keys.edx.keys import AssetKey, CourseKey

from regression.pages.whitelabel.const import (
    ACCESS_TOKEN,
    AUTH_PASSWORD,
    AUTH_USERNAME,
    DEFAULT_GMAIL_USER,
    DEFAULT_TIMEOUT,
    ECOMMERCE_API_URL,
    EMAIL_SENDER_ACCOUNT,
    GMAIL_PASSWORD,
    INITIAL_WAIT_TIME,
    ORG,
    TIME_OUT_LIMIT,
    WAIT_TIME
)


class MailException(Exception):
    """
    Exceptions for Mail failures
    """
    pass


class ApiException(Exception):
    """
    Exceptions for API failures
    """
    pass


class MailClient(object):
    """
    Connect to Gmail clinet using imap and read mails from Inbox
    """

    def __init__(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')

    def login_to_email_account(self):
        """
        Login to gmail account
        """
        self.mail.login(DEFAULT_GMAIL_USER, GMAIL_PASSWORD)

    def open_inbox(self):
        """
        Open inbox to get the list of emails
        """
        self.mail.list()
        # Out: list of "folders" aka labels in gmail.
        self.mail.select("inbox")  # connect to inbox.

    def get_latest_email_uid(self, current_email_user, mail_topic):
        """
        This function will check the availability of target email at the
        intervals of 5 seconds and if the email is found it's uuid is returned.
        If the email is not found after predefined period of time seconds,
        this function will raise an error
        Args:
            current_email_user:
            mail_topic:
        Returns:
            email_uuid:
        """
        self.login_to_email_account()
        self.open_inbox()
        latest_email_uid = None
        t_end = time.time() + TIME_OUT_LIMIT
        # Run the loop for a pre defined time
        time.sleep(INITIAL_WAIT_TIME)
        while time.time() < t_end:
            try:
                # Check that target email is present in Inbox
                # The target mail has to satisfy following criteria
                # a) It has to be sent during the last 24 hours (this is used
                # mainly to speed up the search)
                # b) Mail From and Mail To are correct
                # c) The partial subject string is present in the mail subject
                result, data = self.mail.uid(
                    'search',
                    None,
                    '(SENTSINCE {date} HEADER FROM {mail_from} TO '
                    '{mail_to} SUBJECT {mail_subject})'.format(
                        date=yesterday_date(),
                        mail_from=EMAIL_SENDER_ACCOUNT[ORG],
                        mail_to=current_email_user,
                        mail_subject=mail_topic
                    )
                )
                if not result:
                    raise MailException
                # Get the uid of last email that satisfies the criteria
                latest_email_uid = data[0].split()[-1]
                break
            except MailException:
                time.sleep(WAIT_TIME)
        if latest_email_uid:
            return latest_email_uid
        else:
            raise MailException('No Email matching the search criteria')

    def get_email_message(self, current_email_user, mail_topic):
        """
        Get the text message from Email
        Args:
            current_email_user:
            mail_topic:
        Returns:
            email text:
        """
        resulting_data = self.mail.uid(
            'fetch',
            self.get_latest_email_uid(current_email_user, mail_topic),
            '(RFC822)'
        )
        mail_data = resulting_data[1]
        raw_email = mail_data[0][1]
        email_message = email.message_from_string(raw_email)
        return self.get_first_text_block(email_message)

    @staticmethod
    def get_first_text_block(email_message_instance):
        """
        In case of multiple payloads return first text block
        Args:
            email_message_instance:
        """
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()


def get_target_url_from_text(partial_url_string, text_chunk):
    """
    Search and return the target url from text chunk, the url is searched
    on the basis of partial string embedded in url
    Args:
        partial_url_string:
        text_chunk:
    Returns:
        target url:
    """
    pattern = r"(?P<url>http[s]?://[^\s]+(/{}/)[^\s]+)".format(
        partial_url_string
    )
    regex_result = re.search(pattern, text_chunk)
    if regex_result:
        target_url = regex_result.group("url")
        return target_url.rstrip('.')
    else:
        return 'Target URL not found in the text'


class EcommerceApiClient(object):
    """
    Ecommerce API client for various actions like creating, deleting
    downloading coupons
    """

    @property
    def ecommerce_api_client(self):
        """
        E-Commerce API Client
        """
        return EdxRestApiClient(
            ECOMMERCE_API_URL, oauth_access_token=ACCESS_TOKEN)

    def create_coupon(self, payload):
        """
        Create coupons using API
        Args:
            payload:
        """
        response = self.ecommerce_api_client.coupons.post(data=payload)
        return response['coupon_id']

    def get_coupon_report(self, coupon_id):
        """
        Get coupon report using api
        Args:
            coupon_id:
        """
        return self.ecommerce_api_client.products(coupon_id).get()

    def delete_coupon(self, coupon_id):
        """
        Delete the coupon created in the tests and all associated stock
        records and vouchers.
        Args:
            coupon_id:
        """
        self.ecommerce_api_client.coupons(coupon_id).delete()

    def get_coupon_codes(self, coupon_id):
        """
        Get coupon codes from coupon report
        Args:
            coupon_id:
        """
        coupon_codes = []
        items = (
            self.get_coupon_report(coupon_id)['attribute_values'][0]['value'])
        for item in items:
            coupon_codes.append(item['code'])
        return coupon_codes


def yesterday_date():
    """
    Get and return yesterday's date in dd-mmm-yyyy format
    """
    return (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")


def get_required_cookies(cookies_dict_list):
    """
    Format required cookies
    Args:
        cookies_dict_list:
    """
    response_dict = {}
    for cookie in cookies_dict_list:
        if cookie['name'] == 'ecommerce_csrftoken':
            response_dict.update({'ecommerce_csrftoken': cookie['value']})
        elif cookie['name'] == 'ecommerce_sessionid':
            response_dict.update({'ecommerce_sessionid': cookie['value']})
    required_cookies = '; '.join('{}={}'.format(
        key, val) for key, val in response_dict.items())
    return required_cookies


def get_coupon_request(target_url, cookie_str):
    """
    Send a Get request and return the response if successful
    Args:
      target_url:
      cookie_str:
    """
    kwargs = {}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Cookie': cookie_str
    }
    kwargs.update({
        'headers': headers,
        'auth': HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD),
    })
    response = requests.get(target_url, **kwargs)
    if response.ok:
        return response.content
    else:
        msg = "Could not use restful API.  Status code: {0}".format(
            response.status_code)
        raise ApiException(msg)


def get_enrollment_codes_from_email(coupon_string):
    """
    Read enrollment codes and urls from email
    Ignore first four lines of file as these are just headers
    Args:
        coupon_string:
    Returns:
        coupon codes and urls:
    """
    coupons = {}
    for i, row in enumerate(coupon_string.splitlines()):
        # Read the coupons starting from line 5
        if i > 3:
            if row:
                new_row = row.split(',')
                coupons.update({new_row[0]: new_row[1]})
    if coupons:
        return coupons
    else:
        return 'Coupons not found'


def skip_cleanup_if_test_passed():
    """
    Skip cleanup when tests are passing
    """
    def decorator(test_function):
        """
        Decorator
        Args:
            test_function:
        """
        @functools.wraps(test_function)
        def wrapper(self, *args, **kwargs):
            """
            Wrapper
            Args:
                self:
                *args:
                **kwargs:
            """
            test_function(self, *args, **kwargs)
            self.full_cleanup = False
        return wrapper
    return decorator


def fill_input_fields(page, selectors_and_values_dict):
    """
    A helper function to fill multiple fields in a form
    Args:
        page:
        selectors_and_values_dict:
    """
    for key, value in selectors_and_values_dict.iteritems():
        page.q(css=key).fill(value)


def select_value_from_drop_down(page, drop_down_name, value):
    """
    A helper function to select value from drop down
    Args:
        page:
        drop_down_name:
        value:
    """
    page.wait_for_element_visibility(
        'select[name={}]'.format(drop_down_name), 'Drop down is visible')
    page.q(
        css='select[name={}] option[value="{}"]'.format(drop_down_name, value)
    ).click()
    page.wait_for(
        lambda: page.q(
            css='select[name={}] option[value="{}"]'.
            format(drop_down_name, value)
        ).selected,
        "Correct value is selected",
        timeout=DEFAULT_TIMEOUT
    )


def click_checkbox(page, css_selector):
    """
    A helper function to click check boxes
    Args:
       page:
       css_selector:
    """
    # pylint: disable=unnecessary-lambda
    page.wait_for_element_visibility(css_selector, 'wait for target checkbox')
    page_elem = page.q(css=css_selector).results[0]
    if not page_elem.is_selected():
        page.browser.execute_script("arguments[0].click();", page_elem)
        page.wait_for(
            lambda: page_elem.is_selected(),
            'Target checkbox is selected'
        )


def remove_spaces_from_list_elements(list_with_spaces):
    """
    A helper function to remove spaces from all items in the list
    Args:
      list_with_spaces:
    """
    return [x.replace(' ', '') for x in list_with_spaces]


def get_text_against_page_elements(page, css_selectors):
    """
    A helper function to get text values for a list of web elements
    Args:
        page:
        css_selectors:
    Returns:
        list_of_text:
    """
    list_of_text = []
    for css_selector in css_selectors:
        list_of_text.append(page.q(css=css_selector).text[0])
    return list_of_text


def extract_mmm_dd_yyyy_date_string_from_text(original_string):
    """
    Extract date of MM dd, yyyy from text
    Args:
        original_string:
    Returns:
        date_string
    """
    regex_result = re.search(
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}',
        original_string
    )
    if regex_result:
        date_string = regex_result.group(0)
        return date_string
    else:
        return 'Required date pattern not found in search string'


def convert_date_format(original_date, original_format, required_format):
    """
    Convert dates format to required pattern
    Args:
       original_date:
       original_format:
       required_format:
    Returns:
       modified date:
    """
    try:
        return datetime.datetime.strptime(
            original_date,
            original_format
        ).strftime(required_format)
    except ValueError:
        return 'Invalid date or format'


def extract_numerical_value_from_price_string(raw_price_string):
    """
    Extract numerical value from a string containing price
    Args:
        raw_price_string:
    Returns:
        numerical price:
    """
    regex_result = re.search(
        r'\d+,\d+\.\d+|\d+\.\d+|\d+,\d+|\d+',
        raw_price_string
    )
    if regex_result is not None:
        price_value = regex_result.group(0)
        return float(price_value.replace(",", ""))
    else:
        return 'No numerical value found in search string'


def substring_from(s, delim):
    """
    Get a substring starting from a given delimiter
    Args:
        s: original string
        delim: delimiter
    Returns:
        substring:
    """
    if s.partition(delim)[1]:
        return s.partition(delim)[1] + s.partition(delim)[2]
    else:
        return 'Target substring not found'


def get_course_key_from_asset(asset_string):
    """
    Get course id using asset keys
    Args:
        asset_string:
    Returns:
        course key:
    """
    return AssetKey.from_string(asset_string).course_key


def get_course_number_from_course_id(course_id):
    """
    Get course number from course id using opaque course key
    Args:
        course_id:
    Returns:
        course number:
    """
    return CourseKey.from_string(course_id).course
