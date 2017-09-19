"""
Api clients for tests.
"""
import time
import datetime
import Cookie
import json
import requests
from requests.auth import AuthBase
from edx_rest_api_client.client import EdxRestApiClient
from guerrillamail import GuerrillaMailSession

from regression.tests.helpers.utils import get_org_specific_registration_fields
from regression.pages import (
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LOGIN_EMAIL, LOGIN_PASSWORD
)
from regression.pages.lms import LMS_BASE_URL, LMS_PROTOCOL
from regression.pages.lms import LOGIN_BASE_URL as LMS_AUTH_URL
from regression.pages.studio import STUDIO_BASE_URL, STUDIO_PROTOCOL
from regression.pages.studio import LOGIN_BASE_URL as STUDIO_AUTH_URL
from regression.pages.whitelabel.const import (
    ACCESS_TOKEN,
    EMAIL_SENDER_ACCOUNT,
    INITIAL_WAIT_TIME,
    TIME_OUT_LIMIT,
    WAIT_TIME,
    ENROLLMENT_API_URL,
    ECOMMERCE_API_URL,
    URL_WITHOUT_AUTH,
    URL_WITH_AUTH,
    AUTH_USERNAME,
    AUTH_PASSWORD
)
from regression.pages.common.utils import get_target_url_from_text


class BearerAuth(AuthBase):
    """ Attaches Bearer Authentication to the given Request object. """

    def __init__(self, token):
        """ Instantiate the auth class. """
        self.token = token

    def __call__(self, r):
        """ Update the request headers. """
        r.headers['Authorization'] = 'Bearer {}'.format(self.token)
        return r


class ApiException(Exception):
    """
    Exceptions for API failures
    """
    pass


class MailException(Exception):
    """
    Exceptions for Mail failures
    """
    pass


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


class LogistrationApiBaseClass(object):
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
        browser.get(self.browser_get_url)
        for cookie in self.session.cookies:
            cookie_dict = {
                'name': cookie.name,
                'value': cookie.value,
                'path': cookie.path,
                'expiry': cookie.expires
            }
            # The domain for the sessionid cookie needs to be
            # '.stage.edx.org'. The browser was setting it correctly
            # when logging into lms, but was setting it to
            # 'studio.stage.edx.org' when logging into studio.
            # For studio we need to set domain back to .stage.edx.org
            # but for WL sites we need the to remain as is
            if 'studio' in self.logistration_base_url:
                if cookie.name == 'stage-edx-sessionid':
                    cookie_dict['domain'] = '.stage.edx.org'
            browser.add_cookie(cookie_dict)
        browser.get(self.browser_get_url)


class LogoutApi(object):
    """
    This class uses the cookies from browser session to logout
    current user with the help of api request
    """
    def __init__(self):
        super(LogoutApi, self).__init__()
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
    def __init__(self, target_page=None):
        super(LmsLoginApi, self).__init__()

        target_page_partial_link = target_page or '/dashboard'

        self.logistration_base_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'login'
        )

        self.logistration_post_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'user_api/v1/account/login_session/'
        )

        self.browser_get_url = LMS_AUTH_URL + target_page_partial_link


class StudioLoginApi(LogistrationApiBaseClass):
    """
    Login api for Studio
    """
    def __init__(self):
        super(StudioLoginApi, self).__init__()

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
        super(WLRegisterApi, self).__init__()

        target_page_partial_link = target_page or 'dashboard'

        self.payload = get_org_specific_registration_fields()

        self.logistration_base_url = '{}{}'.format(
            URL_WITHOUT_AUTH,
            'register?next=%2F'
        )

        self.logistration_post_url = '{}{}'.format(
            URL_WITHOUT_AUTH,
            'user_api/v1/account/registration/'
        )

        self.browser_get_url = URL_WITH_AUTH + target_page_partial_link


class GuerrillaMailApi(object):
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
        else:
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


class EnrollmentApiClient(object):
    """
    Enrollment API client
    """

    def __init__(self, host=None, key=None):
        self.host = host or ENROLLMENT_API_URL
        self.key = key or ACCESS_TOKEN

    def is_user_enrolled(self, username, course_id):
        """
        Retrieve the enrollment status for given user in a given course.
        Args:
            username:
            course_id:
        Returns:
            True or false based on whether user is enrolled
        """
        url = '{host}/enrollment/{username},{course_id}'.format(
            host=self.host,
            username=username,
            course_id=course_id
        )
        response = requests.get(url, auth=BearerAuth(self.key))
        check_response(response)
        formatted_response = response.json()
        return formatted_response['is_active']


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
        if 'coupon_id' not in response.keys():
            raise ApiException('Coupon not created')
        return response['coupon_id']

    def get_coupon_report(self, coupon_id):
        """
        Get coupon report using api
        Args:
            coupon_id:
        """
        response = self.ecommerce_api_client.products(coupon_id).get()
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
        response = self.ecommerce_api_client.coupons(coupon_id).delete()
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


class LmsApiClient(object):
    """
    API class for accessing different APIs
    """

    def __init__(self, host=None):
        """
        Instantiate the api class.
        """
        self.host = host or URL_WITHOUT_AUTH
        self.session = requests.Session()
        self.session.auth = (AUTH_USERNAME, AUTH_PASSWORD)
        self.login_response = None

    def _post_headers(self, x_csrf=None):
        """
        Default HTTP headers dict.
        Args:
            x_csrf:
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
        Args:
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

        """
        set_cookie = self.login_response.headers['Set-Cookie']
        if not set_cookie:
            raise ApiException('Login response cookie not found')
        return Cookie.SimpleCookie(set_cookie)

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
        Args:
          target_url:
        """
        response = self.session.get(target_url)
        check_response(response)
        return response.content
