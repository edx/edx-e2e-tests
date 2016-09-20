# -*- coding: utf-8 -*-

"""
Different utilities to be used in tests
"""

import functools
from datetime import datetime
from itertools import izip
import re
import time
import requests
from requests.auth import HTTPBasicAuth

from edx_rest_api_client.client import EdxRestApiClient
from guerrillamail import GuerrillaMailSession
from tempmail import TempMail

from regression.pages.whitelabel.const import (
    ACCESS_TOKEN,
    AUTH_PASSWORD,
    AUTH_USERNAME,
    URL_WITHOUT_AUTH,
    DEFAULT_TIMEOUT,
    ECOMMERCE_URL_WITHOUT_AUTH,
    ECOMMERCE_API_URL,
    EMAIL_SENDER_ACCOUNT,
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


class GuerrillaMailApi(object):
    """
    Guerrilla Mail API for creating email accounts and reading emails
    """

    def __init__(self):
        self.session = GuerrillaMailSession()

    def get_email_account(self, user_name):
        """
        This function will create an account on GuerrillaMail using given user
        name and first of the available domains. The email address created by
        joining user name and domain is returned
        Args:
            user_name:
        Returns:
            email address:
        """
        self.session.set_email_address(user_name)
        return self.session.get_session_state()['email_address']

    def get_email_text(self, pattern):
        """
        This function will check the availability MIT enrollment email at
        GuerrillaMail server at the intervals of 5 seconds and if the email
        is found it's text is returned. If the email is not found after 40
        seconds, this function will raise and error
        Args:
            pattern:
        Returns:
            email text:
        """
        email_text = ""
        t_end = time.time() + TIME_OUT_LIMIT
        # Run the loop for a pre defined time
        time.sleep(INITIAL_WAIT_TIME)
        while time.time() < t_end:
            try:
                # Check that mail box is not empty
                email_list = self.session.get_email_list()
                if not email_list:
                    # raise an exception that waits 3 seconds before
                    # restarting loop
                    raise MailException
                # Get the email id of last email in the inbox
                email_id = email_list[0].guid
                # if last email is not sent by MIT raise the exception
                email = self.session.get_email(email_id)
                if email.sender != EMAIL_SENDER_ACCOUNT[ORG]:
                    raise MailException
                # Fetch the email text and stop the loop
                email_text = email.body
                if pattern not in email_text:
                    raise MailException
                break
            except MailException:
                time.sleep(WAIT_TIME)
        if email_text:
            return email_text
        else:
            raise MailException('No Email from ' + EMAIL_SENDER_ACCOUNT[ORG])


class TempMailApi(object):
    """
    Temp Mail API for creating email accounts and reading emails
    """

    def __init__(self):
        self.session = TempMail()

    def get_email_account(self, user_name):
        """
        This function will create an account on TempMail using given user
        name and first of the available domains. The email address created
        by joining user name and domain is returned
        Args:
            user_name:
        Returns:
            email account:
        """
        self.session.login = user_name
        self.session.domain = self.session.available_domains[0]
        return self.session.get_email_address()

    def get_email_text(self, pattern):
        """
        This function will check the availability MIT enrollment email at
        TempMail server at the intervals of 5 seconds and if the email is
        found it's text is returned. If the email is not found after 40
        seconds, this function will raise and error
        Args:
            pattern:
        Returns:
            email text:
        """
        email_text = ""
        t_end = time.time() + TIME_OUT_LIMIT
        # Run the loop for a pre defined time
        time.sleep(INITIAL_WAIT_TIME)
        while time.time() < t_end:
            try:
                # Check that mail box is not empty
                tmp_email = self.session.get_mailbox()
                if not isinstance(tmp_email, list):
                    raise MailException
                if tmp_email[-1]['mail_from'] != EMAIL_SENDER_ACCOUNT[ORG]:
                    raise MailException
                # Fetch the email text and stop the loop
                email_text = tmp_email[-1]['mail_text']
                if pattern not in email_text:
                    raise MailException
                break
            except MailException:
                time.sleep(WAIT_TIME)
        if email_text:
            return email_text
        else:
            raise MailException('No Email from ' + EMAIL_SENDER_ACCOUNT[ORG])


class EmailReader(object):
    """
    Email reader for reading mail text
    """

    def __init__(self, account):
        self.email = account

    @property
    def activation_link_from_email(self):
        """
        This function will find the activation link embedded in email text and
        returns it
        Returns:
            activation link:
        """
        pattern = URL_WITHOUT_AUTH + 'activate/'
        search_pattern = r'(?<={id})\w+'.format(id=pattern)
        search_activation_code = re.search(
            search_pattern, self.email.get_email_text(pattern))
        activation_code = search_activation_code.group(0)
        activation_link = pattern + activation_code
        return activation_link

    @property
    def reset_password_link_from_email(self):
        """
        This function will find the reset password link embedded in email
        text and returns it
        Returns:
            reset password link:
        """
        pattern = URL_WITHOUT_AUTH + 'password_reset_confirm/'
        search_reset_password_link = re.search(
            pattern + r'(.*?)/', self.email.get_email_text(pattern))
        reset_password_link = search_reset_password_link.group(0)
        return reset_password_link

    @property
    def download_csv_file_link_from_email(self):
        """
        This function will find the download csv file link embedded in
        email text and returns it
        Returns:
            download csv link:
        """
        pattern = 'enrollment_code_csv/'
        search_pattern = r'(?<={})\w+\-\d+/'.format(pattern)
        search_activation_code = re.search(
            search_pattern,
            self.email.get_email_text(pattern)
        )
        order_number = search_activation_code.group(0)
        download_csv_file_link = (
            ECOMMERCE_URL_WITHOUT_AUTH +
            'coupons/' +
            pattern +
            order_number
        )
        return download_csv_file_link

    @property
    def password_from_email(self):
        """
        This function will find the password embedded in email text and
        returns it
        Returns:
            password:
        """
        pattern = 'password: '
        search_pattern = r'(?<={})\w+'.format(pattern)
        search_password = re.search(
            search_pattern,
            self.email.get_email_text(pattern)
        )
        email_password = search_password.group(0)
        return email_password


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


def get_coupons_from_email(coupon_string):
    """
    Read coupon codes and urls from email
    Ignore first two lines of file as these are headers
    Args:
        coupon_string:
    Returns:
        coupon codes and urls:
    """
    coupons = {}
    for i, row in enumerate(coupon_string.splitlines()):
        if i > 3:
            if row:
                new_row = row.split(',')
                coupons.update({new_row[0]: new_row[1]})
    return coupons


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


def fill_input_fields(page, css_selectors, values):
    """
    A helper function to fill multiple fields in a form
    Args:
        page:
        css_selectors:
        values:
    """
    for css_selector, value in izip(css_selectors, values):
        page.q(css=css_selector).fill(value)


def select_value_from_drop_down(page, drop_down_name, value):
    """
    A helper function to select value from drop down
    Args:
        page:
        drop_down_name:
        value:
    """
    page.wait_for_element_visibility(
        'select[name=' + drop_down_name + ']', 'Drop down is visible')
    page.q(
        css='select[name=' + drop_down_name + '] option[value="{}"]'.format(
            value)).click()
    page.wait_for(
        lambda: page.q(
            css='select[name=' + drop_down_name + '] option[value="{}"]'.
            format(value)).selected,
        "Correct value is selected",
        timeout=DEFAULT_TIMEOUT
    )


def select_values_from_drop_downs(page, drop_down_names, values):
    """
    A helper function to select values from multiple drop downs on a page
    Args:
        page:
        drop_down_names:
        values:
    """
    for drop_down_name, value in izip(
            drop_down_names, values
    ):  # pylint: disable=cell-var-from-loop
        page.wait_for_element_visibility(
            'select[name=' + drop_down_name + ']', 'Drop down is visible')
        page.q(
            css='select[name=' + drop_down_name + '] option[value="{}"]'.
            format(value)).click()
        page.wait_for(
            lambda: page.q(
                css='select[name=' + drop_down_name + '] option[value="{}"]'.
                format(value)).selected,
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


def get_text(page, css_selectors):
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


def convert_date_format(target_date):
    """
    Convert date format to 0000-00-00T00:00:00
    Args:
       target_date:
    Returns:
       modified date:
    """
    old_format_date = datetime.strptime(target_date, '%b %d, %Y')
    return old_format_date.strftime('%Y-%m-%dT%H:%M:%S')


def extract_numerical_value(target_str):
    """
    Extract numerical value from a given string
    Args:
        target_str:
    Returns:
        numerical values:
    """
    val = re.search(r'\d+', target_str)
    return int(val.group(0))


def extract_numerical_value_price(raw_price_string):
    """
    Get full price string and return numerical value
    Args:
        raw_price_string:
    Returns:
        numerical price:
    """
    regex_result = re.search(r'(?<=\$)\d+,\d+|\d+', raw_price_string)
    regex_result = regex_result.group(0)
    return int(regex_result.replace(",", ""))
