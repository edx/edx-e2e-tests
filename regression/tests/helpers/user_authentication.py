"""
Common features related to login, Logout, Registration and course activation
"""
import uuid

from bok_choy.web_app_test import WebAppTest

from regression.pages.common.email_client import MailClient
from regression.pages.common.utils import get_target_url_from_text
from regression.pages.whitelabel.activate_account import ActivateAccount
from regression.pages.whitelabel.dashboard_page import DashboardPage
from regression.pages.whitelabel.logistration_page import (
    LoginPage,
    RegistrationPage
)
from regression.pages.whitelabel.logout_page import (
    LogoutPage,
    EcommerceLogoutPage
)
from regression.pages.whitelabel.const import (
    TEST_EMAIL_ACCOUNT,
    ORG,
    PASSWORD,
    REG_INFO,
)


class UserAuthenticationMixin(WebAppTest):
    """
    Mixin for User Authentication
    """

    def setUp(self):
        """
        Setup for all common features
        """
        super(UserAuthenticationMixin, self).setUp()
        # Initialize all page objects
        self.dashboard = DashboardPage(self.browser)
        self.login_page = LoginPage(self.browser)
        self.registration = RegistrationPage(self.browser)

    def login_user(self, user_email):
        """
        Log in the user and go to dashboard page
        Args:
            user_email:
        """
        self.login_page.visit()
        self.login_page.authenticate_user(user_email, PASSWORD, self.dashboard)

    def register_user(self, target_url):
        """
        Register new user
        :param target_url:
        :return:
        """
        self.prepare_and_fill_registration_data()
        self.registration.submit_registration_form_data(target_url)

    def activate_new_user(self):
        """
        Activate new user
        """
        # Check that activation message is appearing on dashboard
        self.assertTrue(self.dashboard.check_activation_message())
        self.account_activation()
        # Check that activation message is no more appearing on dashboard
        self.assertFalse(self.dashboard.check_activation_message())

    def prepare_and_fill_registration_data(self):
        """
        Prepare and fill registration data
        """
        user_name = str(uuid.uuid4().node)
        partial_email_account_name = '+' + user_name
        self.user_email = TEST_EMAIL_ACCOUNT.format(partial_email_account_name)
        self.registration.fill_registration_form(
            self.user_email, PASSWORD, user_name, REG_INFO, ORG)

    def account_activation(self):
        """
        Fetch activation url from email, open the activation link in a new
        window, verify that account is activated
        """
        main_window = self.browser.current_window_handle
        # Get activation link from email
        activation_url = self.get_url_from_email(
            self.user_email,
            'Activate',
            'activate'
        )
        # Open a new window and go to activation link in this window
        self.browser.execute_script("window.open('');")
        self.browser.switch_to.window(self.browser.window_handles[-1])
        self.activate_account = ActivateAccount(self.browser, activation_url)
        self.activate_account.visit()
        # Verify that activation is complete
        self.activate_account.is_account_activation_complete()
        self.browser.close()
        # Switch back to original window and refresh the page
        self.browser.switch_to.window(main_window)
        self.browser.refresh()

    def get_url_from_email(self, user_email, email_subject, matching_string):
        """
        Connect to the email client
        Get text of target email
        fetch desired url from the email text
        Args:
            user_email:
            email_subject:
            matching_string:
        Returns:
            target url:
        """
        self.mail_client = MailClient()
        email_text = self.mail_client.get_email_message(
            user_email,
            email_subject
        )
        return get_target_url_from_text(matching_string, email_text)

    def logout_user_from_lms(self):
        """
        logout user from application
        """
        LogoutPage(self.browser).logout()

    def logout_user_from_ecommerce(self):
        """
        Logout user from ecommerce site
        """
        EcommerceLogoutPage(self.browser).logout_from_ecommerce()
