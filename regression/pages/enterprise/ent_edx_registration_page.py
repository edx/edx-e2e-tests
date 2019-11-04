"""
Enterprise Logistration page
"""
from __future__ import absolute_import

from edxapp_acceptance.pages.lms.login_and_register import CombinedLoginAndRegisterPage
from regression.pages.lms import LOGIN_BASE_URL


class EnterpriseEdxRegistration(CombinedLoginAndRegisterPage):
    """
    This class is an extended class of CombinedLoginAndRegisterPage,
    where we add methods that are different or not used in LMS
    """
    url = LOGIN_BASE_URL + '/register'

    def is_browser_on_page(self):
        """
        Verifies if the enterprise logo is visible on the page
        """
        return self.q(css='.register-button').visible

    def get_enterprise_name(self):
        """
        Returns enterprise name
        """
        return self.q(css='.enterprise-logo').attrs('alt')[0]

    def register(
            self,
            email="",
            password="",
            username="",
            full_name="",
            country="",
            favorite_movie=""):
        """Fills in and submits the registration form.

        Requires that the "register" form is visible.
        This does NOT wait for the next page to load,
        so the caller should wait for the next page
        (or errors if that's the expected behavior.)

        Keyword Arguments:
            email (unicode): The user's email address.
            password (unicode): The user's password.
            username (unicode): The user's username.
            full_name (unicode): The user's full name.
            country (unicode): Two-character country code.

        """
        # Fill in the form
        if email:
            self.q(css="#register-email").fill(email)
        if full_name:
            self.q(css="#register-name").fill(full_name)
        if username:
            self.q(css="#register-username").fill(username)
        if password:
            self.q(css="#register-password").fill(password)
        if country:
            self.q(css="#register-country").results[0].send_keys(country)
        if favorite_movie:
            self.q(css="#register-favorite_movie").fill(favorite_movie)

        # Submit the register form
        self.q(css=".register-button").click()
