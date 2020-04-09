"""
Base class for white label tests
"""
from __future__ import absolute_import

import os

from bok_choy.web_app_test import WebAppTest

from regression.pages.whitelabel.basket_page import BasketPage
from regression.pages.whitelabel.const import LMS_URL
from regression.pages.whitelabel.dashboard_page import DashboardPageExtended
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.login_page import LoginPage
from regression.pages.whitelabel.logout_page import EcommerceLogoutPage
from regression.pages.whitelabel.registration_page import RegisterPageExtended
from regression.tests.helpers.api_clients import LogoutApi, WLRegisterApi


class WhiteLabelTestsBaseClass(WebAppTest):
    """
    Base class for white label tests
    """
    def setUp(self):
        """
        Setup for all common features
        """
        super(WhiteLabelTestsBaseClass, self).setUp()
        # Initialize all page objects
        self.home_page = HomePage(self.browser)
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.login_page = LoginPage(self.browser)
        self.registration_page = RegisterPageExtended(self.browser)
        self.logout_page = EcommerceLogoutPage(self.browser)
        self.basket_page = BasketPage(self.browser)

    def login_user_using_ui(self, email, password):
        """
        Login a user by manually filling the form.
        """
        self.login_page.provide_info(email, password)
        self.dashboard_page.wait_for_page()

    def register_using_api(self, target=None):
        """
        Register a new user using api
        Arguments:
            target: url for page where user should land after registering
        """
        register_user = WLRegisterApi(target_page=target)
        register_user.authenticate(self.browser)
        if target:
            if "account/finish_auth?course_id" in target:
                self.basket_page.wait_for_page()
        else:
            self.dashboard_page.wait_for_page()

    def logout_user_from_lms(self):
        """
        logout user from application
        """
        self.dashboard_page.logout_lms()
        self.home_page.wait_for_page()

    def logout_user_from_ecommerce(self):
        """
        Logout user from ecommerce site
        """
        self.logout_page.visit()

    def logout_from_wl_using_api(self):
        """
        Get cookies from browser and send these cookie to python request to
        logout using api
        """
        logout_api = LogoutApi()
        logout_api.logout_url = os.path.join(LMS_URL, 'logout')
        logout_api.cookies = self.browser.get_cookies()
        logout_api.logout()
