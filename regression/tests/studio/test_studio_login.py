"""
End to end tests for Studio Login
"""
import os
from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.studio.login_studio import StudioLogin


class StudioUserLogin(WebAppTest):
    """
    Test for logging in and navigating to the Studio Home
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

    def test_login(self):
        """
        Test user can login successfully
        """
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page.is_browser_on_page()
