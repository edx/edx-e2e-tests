"""
Studio login page
"""
from edxapp_acceptance.pages.studio.login import LoginPage
from regression.pages.studio import LMS_LOGIN_BASE_URL


class StudioLogin(LoginPage):
    """
    This class is an extended class of LoginPage.
    """
    url = LMS_LOGIN_BASE_URL + '/login'

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return self.q(css='.js-login.login-button').visible
