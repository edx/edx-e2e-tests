"""
Api clients for tests.
"""
import time
import datetime
import re

import requests
from guerrillamail import GuerrillaMailSession

from regression.pages import (
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LOGIN_EMAIL, LOGIN_PASSWORD
)
from regression.pages.lms import LMS_BASE_URL
from regression.pages.lms import LOGIN_BASE_URL as LMS_AUTH_URL
from regression.pages.studio import STUDIO_BASE_URL
from regression.pages.studio import LOGIN_BASE_URL as STUDIO_AUTH_URL
from regression.pages.whitelabel.const import (
    EMAIL_SENDER_ACCOUNT,
    INITIAL_WAIT_TIME,
    TIME_OUT_LIMIT,
    WAIT_TIME
)


class LoginApiBaseClass(object):
    """
    Base class for login api
    """
    def __init__(self):
        self.login_url = None
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
            browser.add_cookie(
                {
                    'name': cookie.name,
                    'value': cookie.value,
                    'path': cookie.path,
                    'expiry': cookie.expires
                }
            )
        browser.get(self.browser_get_url)


class LmsLoginApi(LoginApiBaseClass):
    """
    Login api for LMS
    """
    def __init__(self):
        super(LmsLoginApi, self).__init__()

        self.login_url = 'https://{}/{}'.format(
            LMS_BASE_URL, 'login'
        )

        self.login_post_url = 'https://{}/{}'.format(
            LMS_BASE_URL, 'user_api/v1/account/login_session/'
        )

        self.browser_get_url = LMS_AUTH_URL + '/dashboard'


class StudioLoginApi(LoginApiBaseClass):
    """
    Login api for Studio
    """
    def __init__(self):
        super(StudioLoginApi, self).__init__()

        self.login_url = 'https://{}/{}'.format(
            STUDIO_BASE_URL, 'signin'
        )

        self.login_post_url = 'https://{}/{}'.format(
            STUDIO_BASE_URL, 'login_post'
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
