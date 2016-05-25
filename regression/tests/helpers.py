"""
Test helper functions.
"""
import os


def visit_all(pages):
    """
    Visit each page object in `pages` (an iterable).
    """
    for page in pages:
        print "Visiting: {}".format(page)
        page.visit()


class LoginHelper():
    """
    Helper class to login to the studio.
    """
    def __init__(self):
        pass

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
