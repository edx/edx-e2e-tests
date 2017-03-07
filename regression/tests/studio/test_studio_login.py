"""
End to end tests for Studio Login
"""
import os
from flaky import flaky
from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.logout_studio import StudioLogout


class StudioUserLogin(WebAppTest):
    """
    Test for logging in and out to Studio
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioUserLogin, self).setUp()
        self.studio_login_page = StudioLogin(self.browser)
        self.studio_home_page = DashboardPageExtended(self.browser)
        self.studio_logout_page = StudioLogout(self.browser)

    def test_login(self):
        """
        Verifies that user can login successfully
        """
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page.wait_for_page()

    @flaky  # TODO: See https://openedx.atlassian.net/browse/LT-65
    def test_logout(self):
        """
        Verifies that user can logout successfully
        """
        self.test_login()
        self.studio_home_page.click_logout_button()
        self.studio_logout_page.wait_for_page()
