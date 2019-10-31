"""
End to end tests for Studio Login
"""
from __future__ import absolute_import

import os
from unittest import skip

from bok_choy.web_app_test import WebAppTest

from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.logout_studio import StudioLogout
from regression.pages.studio.studio_home import DashboardPageExtended


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

    @skip("Skip since studio's login/logout now redirects to LMS (ARCH-323)")
    def test_studio_login_logout(self):
        """
        Verifies that user can login and logout successfully
        """
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page.wait_for_page()
        self.studio_home_page.click_logout_button()
        self.studio_logout_page.wait_for_page()
