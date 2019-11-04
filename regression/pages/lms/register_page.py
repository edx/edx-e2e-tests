"""
Register page.
"""
from __future__ import absolute_import

from edxapp_acceptance.pages.lms.login_and_register import CombinedLoginAndRegisterPage
from regression.pages.lms import LOGIN_BASE_URL


class RegisterPageExtended(CombinedLoginAndRegisterPage):
    """
    This class is an extended class of Register Page,
    where we add methods that are different or not used in Register Page
    """
    url = LOGIN_BASE_URL + "/register"

    def register_user(
            self, email="", password="", country="", username="",
            full_name="", terms_of_service=False
    ):
        """Fills in and submits the registration form.

        Requires that the "register" form is visible.
        This does NOT wait for the next page to load,
        so the caller should wait for the next page
        (or errors if that's the expected behavior.)

        Keyword Arguments:
            email (unicode): The user's email address.
            password (unicode): The user's password.
            country (unicode): Two-character country code.
            username (unicode): The user's username.
            full_name (unicode): The user's full name.
            terms_of_service (boolean): If True, agree to the terms of service
            and honor code.

        """
        # Fill in the form
        self.wait_for_element_visibility(
            '#register-email', 'Email field is shown'
        )
        if email:
            self.q(css="#register-email").fill(email)
        if full_name:
            self.q(css="#register-name").fill(full_name)
        if country:
            self.q(
                css="#register-country option[value='{country}']".format(
                    country=country
                )).click()
        if username:
            self.q(css="#register-username").fill(username)
        if password:
            self.q(css="#register-password").fill(password)
        if terms_of_service:
            self.q(css="#register-honor_code").click()

        # Submit it
        self.q(css=".register-button").click()
