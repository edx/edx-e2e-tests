"""
End to end tests for LMS Login
"""
from __future__ import absolute_import

import os

from bok_choy.web_app_test import WebAppTest

from regression.pages.lms import LMS_BASE_URL, LMS_STAGE_BASE_URL
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.login_lms import LmsLogin


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
        cookie_name = 'stage-edx-sessionid'

        if LMS_STAGE_BASE_URL != LMS_BASE_URL:
            cookie_name = 'sessionid'

        self.login_page.visit()
        self.login_page.provide_info(
            self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD
        )

        self.login_page.click_remember_me()
        self.login_page.submit()
        self.dashboard_ext.wait_for_page()
        # When we check the 'remember me' checkbox
        # then edx keeps the session alive for 7 days.
        # In which case, cookie has 'expiry' value of
        # 7 days. If we don't check the 'remember me'
        # then the value of 'expiry' key of cookie will
        # be none.
        self.assertIsNotNone(self.browser.get_cookie(cookie_name)['expiry'])
