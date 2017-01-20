"""
Test helper functions.
"""
import os
import requests

from regression.pages.studio.utils import get_course_key
from regression.pages.studio import BASE_URL
from regression.pages import (
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LOGIN_EMAIL, LOGIN_PASSWORD
)
from regression.pages.lms import LOGIN_BASE_URL


COURSE_ORG = 'COURSE_ORG'
COURSE_NUMBER = 'COURSE_NUMBER'
COURSE_RUN = 'COURSE_RUN'
COURSE_DISPLAY_NAME = 'COURSE_DISPLAY_NAME'


def get_course_info():
    """
    Returns the course info of the course that we use for
    the regression tests.
    """
    return {
        'org': os.environ.get(COURSE_ORG),
        'number': os.environ.get(COURSE_NUMBER),
        'run': os.environ.get(COURSE_RUN),
        'display_name': os.environ.get(
            COURSE_DISPLAY_NAME)
    }


def get_course_display_name():
    """
    Returns the course info of the course that we use for
    the regression tests.
    """
    return os.environ.get(COURSE_DISPLAY_NAME)


def visit_all(pages):
    """
    Visit each page object in `pages` (an iterable).
    """
    for page in pages:
        print "Visiting: {}".format(page)
        page.visit()


def get_url(url_path, course_info):
    """
    Construct a URL to the page within the course.
    """
    course_key = get_course_key(course_info)
    return "/".join([BASE_URL, url_path, unicode(course_key)])


def get_data_id_of_component(page):
    """
    Returns:
        Data usage id for the component
    """
    data_id = page.q(css='.vert-mod .vert.vert-0').attrs('data-id')[0]
    return data_id


class LoginHelper(object):
    """
    Helper class to login to the studio.
    """
    @staticmethod
    def get_login_email():
        """
        Return login email set in environment variable
        """
        login_email = os.environ.get('USER_LOGIN_EMAIL', 'not_set@nothing.com')
        return login_email

    @staticmethod
    def get_login_password():
        """
        Return the login password set in environment variable
        """
        login_password = os.environ.get('USER_LOGIN_PASSWORD', 'no_password')
        return login_password

    @staticmethod
    def login(login_page):
        """
        Takes login page and logs into it.
        """
        login_page.visit()
        login_email = LoginHelper.get_login_email()
        login_password = LoginHelper.get_login_password()
        login_page.login(login_email, login_password)


class LoginApi(object):
    """
    An Api to login the stage.
    """
    def __init__(self):
        self.login_url = 'https://courses.stage.edx.org/login'
        self.session = requests.Session()
        self.session.auth = (
            BASIC_AUTH_USERNAME,
            BASIC_AUTH_PASSWORD
        )
        self.login_response = None

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
        login_post_url = 'https://courses.stage.edx.org/' \
                         'user_api/v1/account/login_session/'
        payload = {
            'email': LOGIN_EMAIL,
            'password': LOGIN_PASSWORD,
            'remember': 'false'
        }
        response = self.session.post(login_post_url, data=payload)
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
        browser.get(LOGIN_BASE_URL + '/dashboard')
        for cookie in self.session.cookies:
            browser.add_cookie(
                {
                    'name': cookie.name,
                    'value': cookie.value,
                    'path': cookie.path,
                    'expiry': cookie.expires
                }
            )
