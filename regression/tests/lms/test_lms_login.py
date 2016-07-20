"""
End to end tests for LMS Login
"""
import os
from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended


class LoginTest(WebAppTest):
    """
    Sample Test for logging in and navigating to Courseware page
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(LoginTest, self).setUp()
        self.login_page = LmsLogin(self.browser)
        self.dashboard_ext = DashboardPageExtended

    def test_login(self):
        """
        Verifies that user can Log in as a staff
        """
        self.login_page.visit()
        self.login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.assertEqual(
            self.login_page.q(
                css='.wrapper-header-courses .header-courses').text[0].lower(),
            'my courses',
            msg='User not logged in as expected.')
