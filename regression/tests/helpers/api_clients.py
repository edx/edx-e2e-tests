"""
Api clients for tests.
"""
import requests

from regression.pages import (
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LOGIN_EMAIL, LOGIN_PASSWORD
)
from regression.pages.lms import LMS_BASE_URL
from regression.pages.lms import LOGIN_BASE_URL as LMS_AUTH_URL
from regression.pages.studio import STUDIO_BASE_URL
from regression.pages.studio import LOGIN_BASE_URL as STUDIO_AUTH_URL


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
