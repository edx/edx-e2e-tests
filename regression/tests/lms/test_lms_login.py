"""
End to end tests for LMS Login
"""
import os
from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.lms_home_page import LmsHome


class LoginTest(WebAppTest):
    """
    Tests for logging in and navigating to Courseware page
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(LoginTest, self).setUp()
        self.login_page = LmsLogin(self.browser)
        self.dashboard_ext = DashboardPageExtended(self.browser)
        self.lms_home = LmsHome(self.browser)

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

    def test_remember_me(self):
        """
        Verifies that user can use Remember Me functionality
        """
        self.login_page.visit()
        self.login_page.provide_info(
            self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD
        )
        cookie_name = '_gali'
        # Cookie not available
        self.assertFalse(self.browser.get_cookie(cookie_name))
        self.login_page.click_remember_me()
        # Cookie available
        self.assertTrue(self.browser.get_cookie(cookie_name))
        self.login_page.submit()
        self.dashboard_ext.wait_for_page()
        self.dashboard_ext.logout_lms()
        # Cookie not available after logout
        self.assertFalse(self.browser.get_cookie(cookie_name))
