"""
Studio login page
"""
from edxapp_acceptance.pages.studio.login import LoginPage
from regression.pages.studio import BASE_URL
from bok_choy.promise import EmptyPromise


class StudioLogin(LoginPage):
    """
    This class is an extended class of LoginPage.
    We are over ridding methods that are different or adding new
    ones as necessary.
    """
    url = BASE_URL + '/signin'

    def fill_field(self, css, value):
        """
        Fill the login form field with the value.
        """
        self.q(css=css).fill(value)

    def login(self, email, password, expect_success=True):
        """
        Attempt to log in using 'email' and 'password'.
        """
        self.fill_field('input#email', email)
        self.fill_field('input#password', password)
        self.q(css='button#submit').first.click()

        # Ensure that we make it to another page
        if expect_success:
            EmptyPromise(
                lambda: "signin" not in self.browser.current_url,
                "redirected from the login page"
            ).fulfill()
