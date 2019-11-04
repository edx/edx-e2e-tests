"""
LMS login page
"""
from __future__ import absolute_import

from edxapp_acceptance.pages.lms.dashboard import DashboardPage
from edxapp_acceptance.pages.lms.login import LoginPage
from regression.pages.lms import LOGIN_BASE_URL


class LmsLogin(LoginPage):
    """
    This class is an extended class of LoginPage,
    where we add methods that are different or not used in LoginPage
    """
    url = LOGIN_BASE_URL + '/login'

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return self.q(css='.js-login.login-button').visible

    def provide_info(self, email, password):
        """
        Fill in login info
        'Username' and 'Password' are the user's credentials
        """
        email_selector = 'input#login-email'
        password_selector = 'input#login-password'

        self.wait_for_element_visibility(
            email_selector, 'Email input area present')
        self.wait_for_element_visibility(
            password_selector, 'Password input are present')

        self.q(css=email_selector).fill(email)
        self.q(css=password_selector).fill(password)
        self.wait_for_ajax()

    def submit(self):
        """
        Submit registration info to create an account.
        """
        self.q(css='.login-button').first.click()

        # The next page is the dashboard; make sure it loads
        dashboard = DashboardPage(self.browser)
        dashboard.wait_for_page()
        return dashboard

    def click_remember_me(self):
        """
        Clicks Remember Me checkbox
        """
        self.q(css='#login-remember').click()
        # Click initiates an ajax call
        self.wait_for_ajax()

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
