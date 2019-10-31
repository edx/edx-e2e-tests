"""
Enterprise Recovery Email feature tests
"""
from __future__ import absolute_import

import uuid

from regression.pages.enterprise.confirm_recovery_email import ConfirmRecoveryEmail
from regression.pages.enterprise.enterprise_const import (
    ENT_PORTAL_PASSWORD,
    ENT_PORTAL_USERNAME
)
from regression.pages.whitelabel.reset_password_page import ResetPassword
from regression.tests.enterprise.ent_test_base import EnterpriseTestBase
from regression.tests.helpers.api_clients import GuerrillaMailApi
from regression.tests.helpers.utils import get_random_password


class TestEnterpriseRecoveryEmail(EnterpriseTestBase):
    """
    Test Enterprise Recovery Email
    """
    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestEnterpriseRecoveryEmail, self).setUp()
        self.user_name = str(uuid.uuid4().node)
        self.temp_mail = GuerrillaMailApi(self.user_name)
        self.user_email = self.temp_mail.user_email

    def test_enterprise_recovery_email(self):
        """
        Scenario: A user is able to set secondary email
        """
        self.lms_login.visit()
        # Enterprise portal flow
        self.login_to_ent_portal(
            ENT_PORTAL_USERNAME,
            ENT_PORTAL_PASSWORD)
        self.access_course()
        self.ent_edx_login.wait_for_page()
        # Register a new enterprise user
        self.register_ent_edx_user()
        self.ent_course_enrollment.wait_for_page()
        self.dashboard.visit()
        # There should be a message to add secondary email account.
        self.assertTrue(self.dashboard.is_secondary_account_message_visible(
            'Add a recovery email'
            ))
        new_password = get_random_password()
        # # Call the fixture to unlink existing account for the user
        # self.addCleanup(self.unlink_account)
        # Add secondary email address in account settings page.
        self.add_recovery_email(self.user_email)
        # Get the secondary email activation url from the email.
        recovery_email_url = self.temp_mail.get_url_from_email(
            'activate_secondary_email'
        )
        self.dashboard.visit()
        # There should be a message to activate secondary email account.
        self.assertTrue(self.dashboard.is_secondary_account_message_visible(
            'Recovery email is not activated yet'
            ))
        recovery_email_page = ConfirmRecoveryEmail(self.browser, recovery_email_url)
        recovery_email_page.visit()
        # Secondary Email Account has been activated.
        self.assertTrue(recovery_email_page.is_secondary_account_activation_complete)
        # Unlink existing account for the user and logout.
        self.unlink_account()
        # login and go to reset password page to reset the password.
        self.logout_from_lms_using_api()
        self.lms_login.visit()
        self.lms_login.send_forgot_password(self.user_email)
        self.assertTrue(
            self.lms_login.is_password_reset_email_message_visible
        )
        # Get reset password url for the email.
        reset_password_url = self.temp_mail.get_url_from_email(
            'password_reset_confirm'
        )
        # Reset password and log back in.
        reset_password = ResetPassword(self.browser, reset_password_url)
        reset_password.visit()
        reset_password.reset_password(new_password)
        self.lms_login.visit()
        self.lms_login.provide_info(self.user_email, new_password)
        self.lms_login.submit()
        self.dashboard.wait_for_page()
        self.user_account.visit()
        self.assertEqual(self.user_email, self.user_account.get_user_email())
