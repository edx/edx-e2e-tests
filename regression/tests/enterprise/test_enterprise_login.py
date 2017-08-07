"""
Enterprise Login tests
"""
import os
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.enterprise.enterprise_logistration_page import (
    EnterpriseLogistration
)
from regression.pages.enterprise.idp_page import IDPLogin
from regression.pages.enterprise.user_account import UserAccountSettings
from regression.pages.enterprise.enterprise_const import (
    ENTERPRISE_NAME,
    IDP_CSS_ID
)
from regression.tests.helpers.api_clients import LmsLoginApi


class TestEnterpriseLogin(WebAppTest):
    """
    Test Enterprise Login
    """

    EDX_USER_EMAIL = os.environ.get('USER_LOGIN_EMAIL')
    EDX_USER_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    IDP_USERNAME = os.environ.get('IDP_USERNAME')
    IDP_PASSWORD = os.environ.get('IDP_PASSWORD')

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestEnterpriseLogin, self).setUp()
        self.browser.maximize_window()
        self.lms_login = LmsLogin(self.browser)
        self.idp_login = IDPLogin(self.browser)
        self.enterprise_logistration = EnterpriseLogistration(self.browser)
        self.dashboard = DashboardPageExtended(self.browser)
        self.user_account = UserAccountSettings(self.browser)

    def test_login_linked_user(self):
        """
        Scenario: To verify that user is able to use idp to login linked
        account
            Given a user has an edx account which is linked to an IDP
            When this user logs in to the IDP account
            Then the user is taken directly to dashboard page without having
            to provide edx credentials
        """
        self.lms_login.visit()
        self.lms_login.click_idp_icon(IDP_CSS_ID)
        # Clicking on idp login should take user to idp site
        self.idp_login.wait_for_page()
        self.idp_login.login_idp_user(self.IDP_USERNAME, self.IDP_PASSWORD)
        # When users logs in to IDP, he is automatically taken to dashboard
        # without having to provide edX credentials
        self.dashboard.wait_for_page()

    def test_login_unlinked_user(self):
        """
        Scenario: To verify that user is able to use idp to login and link
        account
            Given a user has an edx account which is not linked to an IDP
            When this user logs in to the IDP account
            Then the user is taken to the Enterprise where user can provide
            edX credentials
                And providing the edX credentials there logs user in to
                dashboard
                And also link his edX account with IDP
        """
        # Call the fixture to unlink any existing account for the user
        self.login_and_unlink_account()
        # Starts test
        self.lms_login.visit()
        self.lms_login.click_idp_icon(IDP_CSS_ID)
        # Clicking on idp login should take user to idp site
        self.idp_login.wait_for_page()
        self.idp_login.login_idp_user(self.IDP_USERNAME, self.IDP_PASSWORD)
        # When user logs into IDP account he is taken to Enterprise
        # logistration page
        self.enterprise_logistration.wait_for_page()
        self.assertEqual(
            ENTERPRISE_NAME,
            self.enterprise_logistration.get_enterprise_name()
        )
        # Get the current form and if currently registration page is shown
        # toggle to display login page
        current_form = self.enterprise_logistration.current_form
        if current_form == 'register':
            self.enterprise_logistration.toggle_form()
        self.enterprise_logistration.login(
            self.EDX_USER_EMAIL,
            self.EDX_USER_PASSWORD
        )
        self.dashboard.wait_for_page()
        self.dashboard.click_username_dropdown()
        self.dashboard.click_account_settings_link()
        # Verify that in accounts setting user is linked to IDP
        self.user_account.switch_account_settings_tabs('accounts-tab')
        self.assertTrue(self.user_account.is_idp_account_linked(IDP_CSS_ID))

    def login_and_unlink_account(self):
        """
        Unlink IDP Account
        This serves as a fixture for unlinked user test case, it unlinks the
        user before running the tests to make sure that the precondition
        of test is true
        """
        # Login using api and transfer session to browser
        lms_login_api = LmsLoginApi('/account/settings')
        lms_login_api.authenticate(self.browser)
        # Visit account setting page
        # self.user_account.visit()
        self.user_account.switch_account_settings_tabs('accounts-tab')
        # If linked account is found, unlink it
        if self.user_account.is_idp_account_linked(IDP_CSS_ID):
            self.user_account.unlink_idp_account(IDP_CSS_ID)
        # Delete all cookies to simulate logout behavior
        self.browser.delete_all_cookies()
