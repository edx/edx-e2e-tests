"""
Test helper functions/classes.
"""
import os


class LoginHelper():
    """
    Helper class to help login to the studio.
    """
    def __init__(self):
        pass

    @staticmethod
    def build_base_url(mode):
        """
        Static function which changes the BASE_URL according to mode
        argument passed.
        mode argument can get value of LMS for lms or anything else for studio.
        """
        current_url_mode = os.environ.get('CURRENT_URL_MODE', 'not_set')
        if current_url_mode == 'not_set':
            os.environ['CURRENT_URL_MODE'] = mode

        if current_url_mode != mode:
            os.environ['CURRENT_URL_MODE'] = mode
            username = os.environ.get('BASIC_AUTH_USER', 'not_set')
            password = os.environ.get('BASIC_AUTH_PASSWORD', 'not_set')
            if mode == 'LMS':
                os.environ['test_url'] = 'https://{}:{}@courses.stage.edx.org'.format(username, password)
                print os.environ.get('test_url')
            else:
                os.environ['test_url'] = 'https://{}:{}@studio.stage.edx.org'.format(username, password)
                print os.environ.get('test_url')

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
    def get_base_url():
        return os.environ.get('test_url')

    def _get_login_email(self):
        login_email = os.environ.get('USER_LOGIN_EMAIL', 'not_set@nothing.com')
        return login_email

    def _get_login_password(self):
        login_password = os.environ.get('USER_LOGIN_PASSWORD', 'no_password')
        return login_password

    def login(self, login_page):
        login_page.visit()
        login_email = self._get_login_email()
        login_password = self._get_login_password()
        login_page.login(login_email, login_password)