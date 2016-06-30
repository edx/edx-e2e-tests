"""
LMS login page
"""
from edxapp_acceptance.pages.studio.login import LoginPage

from regression.pages.studio import BASE_URL


class StudioLogin(LoginPage):
    """
    This class is an extended class of LoginPage.
    We are overridding methods that are different or adding new
    ones as necessary.
    """
    url = BASE_URL + '/signin'

    def login(self, email, password):
        """
        Attempt to log in using `email` and `password`.
        """
        self.q(css='input#email').fill(email)
        self.q(css='input#password').fill(password)
        self.q(css='button#submit').first.click()

        # Ensure that we make it to another page
        self.wait_for(lambda: 'signin' not in self.browser.current_url,
                      description='Redirected from the login page')
