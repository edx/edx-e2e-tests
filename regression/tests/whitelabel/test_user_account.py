"""
Tests for new users using Otto
"""
from __future__ import absolute_import

import uuid
from unittest import skip

from regression.pages.whitelabel.activate_account import ActivateAccount
from regression.pages.whitelabel.inactive_account import InactiveAccount
from regression.pages.whitelabel.reset_password_page import ResetPassword, ResetPasswordComplete
from regression.tests.helpers.api_clients import GuerrillaMailApi
from regression.tests.helpers.utils import (
    get_random_password, get_white_label_registration_fields
)
from regression.tests.whitelabel.white_label_tests_base import WhiteLabelTestsBaseClass


class TestUserAccount(WhiteLabelTestsBaseClass):
    """
    User Accounts Tests
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestUserAccount, self).setUp()
        self.inactive_account = InactiveAccount(self.browser)
        self.reset_password_complete = ResetPasswordComplete(self.browser)
        user_name = str(uuid.uuid4().node)
        self.temp_mail = GuerrillaMailApi(user_name)

    @skip(
        'This test requires access to gmail,'
        'currently we are using an alternate test'
    )
    def test_activate_account(self):  # TE-2044
        """
        Scenario: A user is able to activate his account
        """
        # Go to registration page and register for the course
        self.home.visit()
        self.home.go_to_registration_page()
        self.register_user(self.dashboard)
        # Check that activation message is appearing on dashboard
        self.assertTrue(self.dashboard.check_activation_message())
        self.account_activation()
        # Check that activation message is no more appearing on dashboard
        self.assertFalse(self.dashboard.check_activation_message())
        # Logout
        self.logout_user_from_lms()

    @skip(
        'This test requires access to gmail,'
        'currently we are using an alternate test'
    )
    def test_reset_password(self):  # TE-2044
        # pylint: disable=no-value-for-parameter
        # pylint: disable=no-member
        # pylint: disable=attribute-defined-outside-init
        """
        Scenario: A user is able to reset the password
        """
        temp_mail = GuerrillaMailApi()
        self.user_name = str(uuid.uuid4().node)
        self.user_email = temp_mail.get_email_account(self.user_name)
        new_password = get_random_password()
        # Got to login page and use the forgot password functionality
        self.login_page.visit()
        self.login_page.send_forgot_password(self.user_email)
        self.assertTrue(
            self.login_page.is_password_reset_email_message_visible
        )
        reset_password_url = self.get_url_from_email(
            self.user_email,
            'password_reset_confirm'
        )
        reset_password = ResetPassword(self.browser, reset_password_url)
        reset_password.visit()
        reset_password.reset_password(new_password)
        self.reset_password_complete.go_to_login_page()
        self.login_page.authenticate_user(
            self.user_email,
            new_password,
        )
        self.dashboard.is_browser_on_page()

    @skip
    def test_activate_account_and_reset_password(self):
        """
        Scenario: A user is able to activate his account
        and afterwards reset the password
        """
        self.home_page.visit()
        self.home_page.click_registration_button()
        self.registration_page.wait_for_page()
        # Register a new user
        self.registration_page.register_white_label_user(
            get_white_label_registration_fields(
                email=self.temp_mail.user_email,
                username=self.temp_mail.user_name
            )
        )
        self.dashboard_page.wait_for_page()
        # There should be a message to activate the account.
        self.assertTrue(self.dashboard_page.is_activation_message_present)
        # Get the activation url from the email.
        activation_url = self.temp_mail.get_url_from_email('activate')
        activate_account_page = ActivateAccount(self.browser, activation_url)
        activate_account_page.visit()
        # Account has been activated.
        self.assertTrue(activate_account_page.is_account_activation_complete)
        # Go back to the dashboard page and assert
        #  that activation is successful.
        activate_account_page.click_dashboard_from_drop_down_menu()
        self.dashboard_page.wait_for_page()
        self.assertFalse(self.dashboard_page.is_activation_message_present)
        # logout and go to reset password page to reset the password.
        self.dashboard_page.logout_lms()
        self.home_page.wait_for_page()
        self.home_page.click_login_button()
        self.login_page.wait_for_page()
        self.login_page.send_forgot_password(self.temp_mail.user_email)
        self.assertTrue(
            self.login_page.is_password_reset_email_message_visible
        )
        # Get reset password url for the email.
        reset_password_url = self.temp_mail.get_url_from_email(
            'password_reset_confirm'
        )
        new_password = get_random_password()
        reset_password_page = ResetPassword(self.browser, reset_password_url)
        reset_password_page.visit()
        # Reset password and log back in.
        reset_password_page.reset_password(new_password)
        reset_password_complete = ResetPasswordComplete(self.browser)
        reset_password_complete.click_login_button()
        self.login_page.wait_for_page()
        self.login_page.provide_info(self.temp_mail.user_email, new_password)
        self.login_page.submit()
        self.dashboard_page.wait_for_page()
