from bok_choy.promise import EmptyPromise
from edxapp_pages.lms.login import LoginPage
from edxapp_pages.lms.dashboard import DashboardPage
from . import BASE_URL


class LmsLoginPage(LoginPage):
    """
    Extended class of LoginPage from LmsLoginPage
    """

    url = BASE_URL + '/login'

    def is_browser_on_page(self):
        return self.q(css='.action.action-primary.action-update.js-login.login-button').present

    def provide_info(self, email, password):
        """
        Fill in login info.
        `email` and `password` are the user's credentials.
        """
        EmptyPromise(self.q(css='input#login-email').is_present, "Click ready").fulfill()
        EmptyPromise(self.q(css='input#login-password').is_present, "Click ready").fulfill()

        self.q(css='input#login-email').fill(email)
        self.q(css='input#login-password').fill(password)
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
