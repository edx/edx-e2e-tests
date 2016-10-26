"""
Login page for LMS
"""
from bok_choy.page_object import PageObject

from regression.pages.common.utils import (
    click_checkbox,
    fill_input_fields,
    select_value_from_drop_down
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
        elements_and_values = {
            '#login-email': email,
            '#login-password': password
        }
        fill_input_fields(self, elements_and_values)
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
        ).filter(lambda elem: elem.text == 'Check Your Email').visible

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
        elements_and_values = {
            '#register-email': email,
            '#register-name': reg_info['full_name'],
            '#register-username': username,
            '#register-password': password,
            '#register-first_name': reg_info['first_name'],
            '#register-last_name': reg_info['last_name'],
            '#register-state': reg_info['state']
        }
        fill_input_fields(self, elements_and_values)
        select_names_and_values = {
            "country": reg_info['country'],
            "year_of_birth": reg_info['yob'],
        }
        for key, val in select_names_and_values.iteritems():
            select_value_from_drop_down(self, key, val)
        if org != 'HarvardXPLUS':
            select_names_and_values = {
                "gender": reg_info['gender'],
                "level_of_education": reg_info['edu_level']
            }
            for key, val in select_names_and_values.iteritems():
                select_value_from_drop_down(self, key, val)
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
