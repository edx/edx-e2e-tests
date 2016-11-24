"""
LMS login page
"""
from edxapp_acceptance.pages.lms.login import LoginPage
from edxapp_acceptance.pages.lms.dashboard import DashboardPage
from regression.pages.lms import BASE_URL


class LmsLogin(LoginPage):
    """
    This class is an extended class of LoginPage,
    where we add methods that are different or not used in LoginPage
    """
    url = BASE_URL + '/login'

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
