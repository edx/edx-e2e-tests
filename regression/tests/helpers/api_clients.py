"""
Api clients for tests.
"""
import time
import datetime
import re
import Cookie
import json
import requests
from requests.auth import AuthBase
from edx_rest_api_client.client import EdxRestApiClient
from guerrillamail import GuerrillaMailSession

from regression.pages import (
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LOGIN_EMAIL, LOGIN_PASSWORD
)
from regression.pages.lms import LMS_BASE_URL, LMS_PROTOCOL
from regression.pages.lms import LOGIN_BASE_URL as LMS_AUTH_URL
from regression.pages.studio import STUDIO_BASE_URL, STUDIO_PROTOCOL
from regression.pages.studio import LOGIN_BASE_URL as STUDIO_AUTH_URL
from regression.pages.whitelabel.const import (
    EMAIL_SENDER_ACCOUNT,
    INITIAL_WAIT_TIME,
    TIME_OUT_LIMIT,
    WAIT_TIME,
    ENROLLMENT_API_URL,
    ACCESS_TOKEN,
    ECOMMERCE_API_URL,
    URL_WITHOUT_AUTH,
    AUTH_USERNAME,
    AUTH_PASSWORD
)


class UserSessionApiBaseClass(object):
    """
    Base class for login api
    """
    def __init__(self):
        self.login_url = None
        self.logout_url = None
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

        self.login_response = None
        self.login_post_url = None
        self.browser_get_url = None

    def check_response(self, response):
        """
        Check whether a response was successful. If not raise an exception

        Arguments:
            response: HTTP response object
        """
        if response.status_code != 200:
            raise Exception(
                'API request failed with following error code: ' +
                str(response.status_code)
            )

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
            'Referer': self.login_url,
            'X-CSRFToken': x_csrf,
        }

    def create_base_session(self):
        """
        Create a session with the host.
        """
        response = self.session.get(self.login_url)
        self.check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self.post_headers(
            response.cookies['csrftoken']
        )

    def login(self):
        """
        Login to the stage.
        """
        self.create_base_session()

        response = self.session.post(self.login_post_url, data=self.payload)
        self.check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self.post_headers(
            response.cookies['csrftoken']
        )
        self.login_response = response

    def authenticate(self, browser):
        """
        Authenticate the user and pass the session to the browser.

        Arguments:
        browser: Browser to pass the session to.
        """
        self.login()
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
            if cookie.name == 'stage-edx-sessionid':
                cookie_dict['domain'] = '.stage.edx.org'
            browser.add_cookie(cookie_dict)
        browser.get(self.browser_get_url)

    def logout(self):
        """
        Logout existing user
        """
        self.session.get(self.logout_url)


class LmsSessionApi(UserSessionApiBaseClass):
    """
    Login api for LMS
    """
    def __init__(self, target_page='/dashboard'):
        super(LmsSessionApi, self).__init__()

        target_page_name = target_page

        self.login_url = '{}://{}/{}'.format(
            LMS_PROTOCOL, LMS_BASE_URL, 'login'
        )

        self.login_post_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'user_api/v1/account/login_session/'
        )

        self.logout_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'logout'
        )

        self.browser_get_url = LMS_AUTH_URL + target_page_name


class StudioSessionApi(UserSessionApiBaseClass):
    """
    Login api for Studio
    """
    def __init__(self):
        super(StudioSessionApi, self).__init__()

        self.login_url = '{}://{}/{}'.format(
            STUDIO_PROTOCOL, STUDIO_BASE_URL, 'signin'
        )

        self.login_post_url = '{}://{}/{}'.format(
            STUDIO_PROTOCOL, STUDIO_BASE_URL, 'login_post'
        )

        self.browser_get_url = STUDIO_AUTH_URL + '/home'


class MailException(Exception):
    """
    Exceptions for Mail failures
    """
    pass


def yesterday_date():
    """
    Get and return yesterday's date in dd-mmm-yyyy format
    """
    return (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")


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

    def get_target_url_from_text(self, url_matching_string, text_chunk):
        """
        Search and return the target url from text chunk, the url is searched
        on the basis of partial string embedded in url
        Args:
            url_matching_string:
            text_chunk:
        Returns:
            target url:
        """
        pattern = r"(?P<url>http[s]?://[^\s\"]+(/{}/)[^\s\"]+)".format(
            url_matching_string
        )
        regex_result = re.search(pattern, text_chunk)
        if regex_result:
            target_url = regex_result.group("url")
            return target_url.rstrip('.')
        else:
            return 'Target URL not found in the text'

    def get_url_from_email(self, matching_string):
        """
        Connect to the email client
        Get text of target email
        fetch desired url from the email text
        Args:
            user_email:
            matching_string:
        Returns:
            target url:
        """
        email_text = self.get_email_text(
            self.user_email
        )
        return self.get_target_url_from_text(matching_string, email_text)


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


def check_response(response):
    """
    Check whether a response was successful. If not raise an exception
    Args:
        response:
    """
    if response.status_code != 200:
        raise ApiException(
            'API request failed with following error code: ' +
            str(response.status_code)
        )


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
