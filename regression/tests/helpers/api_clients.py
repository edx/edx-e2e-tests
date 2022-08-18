"""
Api clients for tests.
"""

import datetime
import json
import os
import re
import time

from http import cookies as http_cookies
from urllib.parse import urlparse
import requests
from requests.auth import AuthBase

from edx_rest_api_client.client import EdxRestApiClient
from guerrillamail import GuerrillaMailSession

from regression.pages import (
    BASIC_AUTH_PASSWORD,
    BASIC_AUTH_USERNAME,
    LOGIN_EMAIL,
    LOGIN_PASSWORD
)
from regression.pages.common.utils import get_target_url_from_text
from regression.pages.lms import LMS_BASE_URL, LMS_PROTOCOL
from regression.pages.lms import LOGIN_BASE_URL as LMS_AUTH_URL
from regression.pages.studio import LOGIN_BASE_URL as STUDIO_AUTH_URL
from regression.pages.studio import STUDIO_BASE_URL, STUDIO_PROTOCOL
from regression.pages.whitelabel import LMS_URL, LMS_URL_WITH_AUTH
from regression.pages.whitelabel.const import (
    ECOMMERCE_API_URL,
    EMAIL_SENDER_ACCOUNT,
    ENROLLMENT_API_URL,
    INITIAL_WAIT_TIME,
    OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET,
    TIME_OUT_LIMIT,
    WAIT_TIME
)
from regression.tests.helpers.utils import get_org_specific_registration_fields

OAUTH_ACCESS_TOKEN_URL = os.path.join(LMS_URL_WITH_AUTH, 'oauth2/access_token')


class BearerAuth(AuthBase):
    """ Attaches Bearer Authentication to the given Request object. """

    def __init__(self, token):
        """ Instantiate the auth class. """
        self.token = token

    def __call__(self, r):
        """ Update the request headers. """
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


class ApiException(Exception):
    """
    Exceptions for API failures
    """


class MailException(Exception):
    """
    Exceptions for Mail failures
    """


def check_response(response):
    """
    Check whether a response was successful. If not raise an exception
    Args:
        response:
    """
    if response.status_code != 200:
        raise ApiException(
            'API request failed with following message: ' +
            str(response.text)
        )


def yesterday_date():
    """
    Get and return yesterday's date in dd-mmm-yyyy format
    """
    return (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")


class LogistrationApiBaseClass:
    """
    Base class for logistration api
    """
    def __init__(self):
        self.logistration_base_url = ''
        self.session = requests.Session()
        self.session.auth = (
            BASIC_AUTH_USERNAME,
            BASIC_AUTH_PASSWORD
        )

        self.payload = {
            'email': LOGIN_EMAIL,
            'password': LOGIN_PASSWORD,
            'remember': 'false'
        }

        self.logistration_response = None
        self.logistration_post_url = ''
        self.browser_get_url = ''

    def post_headers(self, x_csrf):
        """
        Header which are to be used in the POST Requests

        Arguments:
            x_csrf: Cross site request forgery protection token.
        """
        return {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.logistration_base_url,
            'X-CSRFToken': x_csrf,
        }

    def create_base_session(self):
        """
        Create a base session with the host.
        """
        response = self.session.get(self.logistration_base_url)
        check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self.post_headers(
            response.cookies['csrftoken']
        )

    def create_user_session(self):
        """
        Create session of a user by registering or logging in
        """
        self.create_base_session()
        response = self.session.post(
            self.logistration_post_url,
            data=self.payload
        )
        check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self.post_headers(
            response.cookies['csrftoken']
        )
        self.logistration_response = response

    def get_cookie_domain(self, url):
        """
        Args:
            url: url to extract cookie domain from

        Returns: cookie domain by striping first sub-domain from domain of give url
            i.e.
            https://courses.stage.edx.org -> .stage.edx.org
            https://studio-test.sandbox.edx.org -> .sandbox.edx.org
            https://courses.edx.org -> .edx.org

        """
        parsed_uri = urlparse(url)
        domain = parsed_uri.netloc.split(':')[0]   # strip off port when tests are run from devstack
        count = len(domain.split('.'))
        cookie_domain = '.'.join(domain.split('.')[1-count:])
        return '.' + cookie_domain

    def authenticate(self, browser):
        """
        Authenticate the user and pass the session to the browser.

        Arguments:
            browser: Browser to pass the session to.
        """
        self.create_user_session()
        # To make cookies effective, we have to set the
        # domain of the browser the same as that of the
        # cookies. To do this, just visit a page of the
        # same domain.
        # Cookies require the domain to be ".stage.edx.org"
        # Browser will navigate to the login page, but
        # no one is required to login. Once cookies become
        # effective, we don't need to login.
        print ("url is " + self.browser_get_url)
        browser.get(self.browser_get_url)
        for cookie in self.session.cookies:
            cookie_dict = {
                'name': cookie.name,
                'value': cookie.value,
                'path': cookie.path,
                'expiry': cookie.expires,
            }
            # The domain for the sessionid cookie needs to be set to
            # '.stage.edx.org' when tests are run with stage urls
            # and '.devstack.edx' when tests are run in devstack
            # for both studio and lms.
            # However, for WL sites we need the to remain as is
            if re.search(r'edx.org|devstack', self.logistration_base_url) and 'sessionid' in cookie.name:
                cookie_dict['domain'] = self.get_cookie_domain(self.logistration_base_url)

            browser.delete_cookie(cookie.name)
            browser.add_cookie(cookie_dict)
        browser.get(self.browser_get_url)


class LogoutApi:
    """
    This class uses the cookies from browser session to logout
    current user with the help of api request
    """
    def __init__(self):
        super().__init__()
        self.logout_url = None
        self.cookies = {}
        self.session = requests.Session()
        self.session.auth = (BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)

    def logout(self):
        """
        Logout from application using api
        """
        self.session.cookies.update(
            {cookie['name']: cookie['value'] for cookie in self.cookies}
        )
        response = self.session.get(self.logout_url)
        check_response(response)


class LmsLoginApi(LogistrationApiBaseClass):
    """
    Logged in session api for LMS
    """
    def __init__(self):
        super().__init__()

        self.logistration_base_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'login?skip_authn_mfe=true'
        )

        self.logistration_post_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'user_api/v1/account/login_session/'
        )

        self.browser_get_url = LMS_AUTH_URL

    def get_offer_request(self, target_url):
        """
        Send a Get request and return the response if successful
        Arguments:
          target_url:
        """
        response = self.session.get(target_url)
        check_response(response)
        return response.content


class StudioLoginApi(LogistrationApiBaseClass):
    """
    Login api for Studio
    """
    def __init__(self):
        super().__init__()

        self.logistration_base_url = '{}://{}/{}'.format(
            STUDIO_PROTOCOL, STUDIO_BASE_URL, 'signin'
        )

        self.logistration_post_url = '{}://{}/{}'.format(
            STUDIO_PROTOCOL, STUDIO_BASE_URL, 'login_post'
        )

        self.browser_get_url = STUDIO_AUTH_URL + '/home'


class WLRegisterApi(LogistrationApiBaseClass):
    """
    Register a new user using API
    """
    def __init__(self, target_page=None):
        super().__init__()

        partial_url_string = target_page or 'dashboard'

        self.payload = get_org_specific_registration_fields()

        self.logistration_base_url = '{}{}'.format(
            LMS_URL,
            '/register?next=%2F&?skip_authn_mfe=true'
        )

        self.logistration_post_url = '{}{}'.format(
            LMS_URL,
            '/user_api/v1/account/registration/'
        )

        self.browser_get_url = os.path.join(
            LMS_URL_WITH_AUTH,
            partial_url_string
        )


class GuerrillaMailApi:
    """
    Api for using Guerrilla Mail.
    """
    def __init__(self, user_name):
        self.session = GuerrillaMailSession()
        self.user_name = user_name
        self.session.set_email_address(self.user_name)
        self.user_email = self.session.get_session_state()['email_address']

    def get_email_text(self, pattern):
        """
        Get email text from GuerrillaMail server.

        Checks the latest email from the inbox and searches for pattern in it.
        If pattern is found then email's body is returned otherwise exception
        is raised. Also, if latest email is not from MIT, it raises exception.

        Checks GuerrillaMail server for email at the intervals of 5 seconds.
        If the email is not found after 40 seconds then exception is raised.

        Arguments:
            pattern(str): Pattern to be found in the email's body.

        Returns:
            str: Email's body.
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
                    # raise an exception that waits 3 seconds
                    # before restarting loop
                    raise MailException
                # Get the email id of last email in the inbox
                email_id = email_list[0].guid
                # if last email is not sent by MIT raise the exception
                email = self.session.get_email(email_id)
                if email.sender != EMAIL_SENDER_ACCOUNT:
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
        raise MailException('No Email from ' + EMAIL_SENDER_ACCOUNT)

    def get_url_from_email(self, matching_string):
        """
        Connect to the email client
        Get text of target email
        fetch desired url from the email text
        Args:
            matching_string:
        Returns:
            target url:
        """
        email_text = self.get_email_text(
            self.user_email
        )
        return get_target_url_from_text(matching_string, email_text)


class EdxRestApiBaseClass:
    """
    Base class for creating EdxRestAPiClient instance
    """
    api_url_root = None
    append_slash = True

    def __init__(self):
        assert self.api_url_root
        access_token, __ = self.get_access_token()
        self.client = EdxRestApiClient(
            self.api_url_root,
            jwt=access_token,
            append_slash=self.append_slash
        )

    @staticmethod
    def get_access_token():
        """ Returns an access token and expiration date from the OAuth
        provider.
        Returns:
            (str, datetime):Tuple containing access token and expiration date.
        """
        return EdxRestApiClient.get_oauth_access_token(
            OAUTH_ACCESS_TOKEN_URL,
            OAUTH_CLIENT_ID,
            OAUTH_CLIENT_SECRET,
            token_type='jwt'
        )


class EcommerceApiClient(EdxRestApiBaseClass):
    """
    Ecommerce API client for various actions like creating, deleting
    downloading coupons
    """

    api_url_root = ECOMMERCE_API_URL

    def get_course_products(self, course_id):
        """
        Get course products
        Arguments:
            course_id
        """
        response = self.client.courses(course_id).products.get()["results"]
        if not response:
            raise ApiException('No course product found')
        return response

    def get_stock_record_id(self, course_id, course_title):
        """
        Get stock record id from course report
        Arguments:
            course_id
            course_title
        """
        product_title = "Seat in {} with professional certificate".format(
            course_title
        )
        stock_record_id = []
        for item in self.get_course_products(course_id):
            if item["stockrecords"] and item["title"].lower() == \
                    product_title.lower():
                stock_record_id.append(item["stockrecords"][0]["id"])
                break
        return stock_record_id

    def create_coupon(self, payload):
        """
        Create coupons using API
        Args:
            payload:
        """
        response = self.client.coupons.post(data=payload)
        if 'coupon_id' not in list(response.keys()):
            raise ApiException('Coupon not created')
        return response['coupon_id']

    def get_coupon_report(self, coupon_id):
        """
        Get coupon report using api
        Args:
            coupon_id:
        """
        response = self.client.products(coupon_id).get()
        if not response:
            raise ApiException('No coupon report found')
        return response

    def delete_coupon(self, coupon_id):
        """
        Delete the coupon created in the tests and all associated stock
        records and vouchers.
        Args:
            coupon_id:
        """
        response = self.client.coupons(coupon_id).delete()
        if not response:
            raise ApiException('Failed to delete the coupon using API')

    def get_coupon_codes(self, coupon_id):
        """
        Get coupon codes from coupon report
        Args:
            coupon_id:
        """
        coupon_codes = []
        items = (
            self.get_coupon_report(coupon_id)['attribute_values'][0]['value']
        )
        for item in items:
            coupon_codes.append(item['code'])
        return coupon_codes


class EnrollmentApiClient(EdxRestApiBaseClass):
    """
    Enrollment API client
    """

    api_url_root = ENROLLMENT_API_URL
    append_slash = False

    def is_user_enrolled(self, username, course_run_id):
        """
        Get enrollment details for the given user and course run.
        Arguments:
            username (str): user name for enrolled user
            course_run_id (str): course id in which user is enrolled
        """
        response = self.client.enrollment(
            f'{username},{course_run_id}'
        ).get()
        check_response(response)
        formatted_response = response.json()
        return formatted_response['is_active']


class LmsApiClient:
    """
    API class for accessing different APIs
    """

    def __init__(self, host=None):
        """
        Instantiate the api class.
        """
        self.host = host or LMS_URL
        self.session = requests.Session()
        self.session.auth = (BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)
        self.login_response = None

    def _post_headers(self, x_csrf=None):
        """
        Default HTTP headers dict.
        Arguments:
            x_csrf: csrf token value
        """
        return {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.host,
            'X-CSRFToken': x_csrf,
        }

    def create_base_session(self):
        """
        Open target site using requests and return cookies
        Returns:
            cookies
        """
        response = self.session.get(self.host)
        check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self._post_headers(
            response.cookies['csrftoken']
        )

    def create_login_session(self, user_email, user_password):
        """
        Create a session and assign cookies to it after successful login
        Arguments:
            user_email:
            user_password:
        """
        self.create_base_session()
        login_url = self.host + 'user_api/v1/account/login_session/'
        payload = {
            'email': user_email,
            'password': user_password,
            'remember': 'false'
        }
        response = self.session.post(login_url, data=payload)
        check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self._post_headers(
            response.cookies['csrftoken']
        )
        self.login_response = response

    @property
    def login_response_cookies(self):
        """
        get cookie info from response headers
        Returns:
            Cookie info: Cookie information in simple cookie format
        """
        set_cookie = self.login_response.headers['Set-Cookie']
        if not set_cookie:
            raise ApiException('Login response cookie not found')
        return http_cookies.SimpleCookie(set_cookie)

    @property
    def user_name(self):
        """
        Extract user name from response
        Returns:
            username
        """
        user_info = self.login_response_cookies['stage-edx-user-info'].value
        user_info_dict = json.loads(user_info)
        if not user_info_dict:
            raise ApiException('User Info Dictionary not found')
        return user_info_dict['username']

    def change_enrollment(self, course_id, enrollment_action):
        """
        Change enrollment
        Args:
            course_id:
            enrollment_action:
        """
        change_enrollment_url = self.host + 'change_enrollment'
        payload = {
            'course_id': course_id,
            'enrollment_action': enrollment_action
        }
        response = self.session.post(
            change_enrollment_url,
            data=payload
        )
        check_response(response)

    def get_coupon_request(self, target_url):
        """
        Send a Get request and return the response if successful
        Arguments:
          target_url:
        """
        response = self.session.get(target_url)
        check_response(response)
        return response.content
