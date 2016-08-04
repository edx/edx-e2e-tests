"""
Test helper functions.
"""
import os

from regression.pages.studio.utils import get_course_key
from regression.pages.studio import BASE_URL


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
