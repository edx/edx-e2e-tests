"""
LMS login page
"""
from __future__ import absolute_import

import os

from bok_choy.page_object import PageObject

from regression.pages.common.utils import fill_input_fields
from regression.pages.whitelabel import LMS_URL_WITH_AUTH


class LoginPage(PageObject):
    """
    Login page for LMS.
    """
    url = os.path.join(LMS_URL_WITH_AUTH, 'login')

    def is_browser_on_page(self):
        return self.q(css='.form-toggle[data-type="register"]').visible

    def provide_info(self, email, password):
        """
        Fill in login info

        Arguments:
            email(str): User's email
            password(str): User's password
        """
        elements_and_values = {
            '#login-email': email,
            '#login-password': password
        }
        fill_input_fields(self, elements_and_values)
        self.wait_for_ajax()
        self.submit()

    def submit(self):
        """
        Submit registration info to create an account.
        """
        self.q(css='.login-button').first.click()

    def send_forgot_password(self, email):
        """
        Send forget password email.

        Arguments:
             email(str): Email to send forget password to.
        """
        self.q(css='.forgot-password.field-link').click()
        self.wait_for_element_visibility(
            '#password-reset', 'Wait for Reset Password form'
        )
        self.q(css='#password-reset-email').fill(email)
        self.q(css='.action.action-primary.action-update.js-reset').click()
        self.wait_for_ajax()

    @property
    def is_password_reset_email_message_visible(self):
        """
        Verify that message for password reset email is visible

        Returns:
            bool: True if message is visible.
        """
        return self.q(
            css='.message-title'
        ).filter(lambda elem: elem.text == 'Check Your Email').visible

    def toggle_to_registration_page(self):
        """
        Toggle to registration page.
        """
        self.q(css='.form-toggle[data-type="register"]').click()

    def authenticate_user(self, email, password):
        """
        Provide email and password for an existing user and log in
        Args:
            email
            password
        """
        elements_and_values = {
            '#login-email': email,
            '#login-password': password
        }
        fill_input_fields(self, elements_and_values)
        self.q(
            css='.action.action-primary.action-update.js-login.login-button'
        ).click()
