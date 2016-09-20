"""
Login page for LMS
"""
from bok_choy.page_object import PageObject

from regression.pages.common.utils import (
    click_checkbox,
    fill_input_fields,
    select_values_from_drop_downs
)
from regression.pages.whitelabel.const import URL_WITH_AUTH


class LoginPage(PageObject):
    """
    Login Page
    """

    url = URL_WITH_AUTH + 'login'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if toggle to registration button is visible
        """
        return self.q(css='.nav-btn.form-toggle[data-type="register"]').visible

    def authenticate_user(self, email, password, target_page):
        """
        Provide email and password for an existing user and log in
        Args:
            email:
            password:
            target_page:
        """
        css_selectors = ['#login-email', '#login-password']
        values = [email, password]
        fill_input_fields(self, css_selectors, values)
        self.q(
            css='.action.action-primary.action-update.js-login.login-button'
        ).click()
        target_page.wait_for_page()

    def send_forgot_password(self, email):
        """
        Provide email to forgot password field
        Args:
             email:
        """
        self.q(css='.forgot-password.field-link').click()
        self.wait_for_element_visibility(
            '#password-reset', 'Wait for Reset Password form'
        )
        self.q(css='#password-reset-email').fill(email)
        self.q(css='.action.action-primary.action-update.js-reset').click()
        self.wait_for_ajax()

    def is_password_reset_email_message_visible(self):
        """
        verify that message for password reset email is visible
        Returns:
            True if message is visible:
        """
        return self.q(
            css='.message-title'
        ).filter(lambda elem: elem.text == 'Password Reset Email Sent').visible

    def toggle_to_registration_page(self):
        """
        Toggle to login page
        """
        self.q(css='.nav-btn.form-toggle[data-type="register"]').click()
        RegistrationPage(self.browser).wait_for_page()


class RegistrationPage(PageObject):
    """
    Registration page
    """

    url = None

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if toggle to login button is visible
        """
        return self.q(css='.nav-btn.form-toggle[data-type="login"]').visible

    def fill_registration_form(self, email, password, username, reg_info, org):
        """
        Fill the registration from using the values from test
        Args:
            email:
            password:
            username:
            reg_info:
            org:
        """
        self.wait_for_element_visibility(
            '.register-form', 'Wait for registration form')
        fill_css_selectors = [
            '#register-email',
            '#register-name',
            '#register-username',
            '#register-password',
            '#register-first_name',
            '#register-last_name',
            '#register-state'
        ]
        fill_values = [
            email,
            reg_info['full_name'],
            username,
            password,
            reg_info['first_name'],
            reg_info['last_name'],
            reg_info['state']
        ]
        fill_input_fields(self, fill_css_selectors, fill_values)
        select_css_selectors = [
            "country",
            "gender",
            "year_of_birth",
            "level_of_education"
        ]
        select_values = [
            reg_info['country'],
            reg_info['gender'],
            reg_info['yob'],
            reg_info['edu_level']
        ]
        select_values_from_drop_downs(
            self, select_css_selectors, select_values)
        if org == 'MITProfessionalX':
            self.q(css='#register-company').fill(reg_info['company'])
            self.q(css='#register-title').fill(reg_info['title'])
            click_checkbox(self, '#register-honor_code')
        click_checkbox(self, '#register-terms_of_service')

    def submit_registration_form_data(self, target_page):
        """
        Submit the registration data and go to target page
        Args:
             target_page:
        """
        self.q(
            css='.action.action-primary.action-update.js-register.'
            'register-button').click()
        target_page.wait_for_page()

    def toggle_to_login_page(self):
        """
        Toggle to login page
        """
        self.q(css='.nav-btn.form-toggle[data-type="login"]').click()
        LoginPage(self.browser).wait_for_page()
