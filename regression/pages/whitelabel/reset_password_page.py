"""
Reset Password page
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH


class ResetPassword(PageObject):
    """
    Reset password
    """

    def __init__(self, browser, reset_password_url):
        """
        Reset Password url has to be set by the test
        """
        super(ResetPassword, self).__init__(browser)
        self.reset_password_url = reset_password_url

    @property
    def url(self):
        """
        Construct a URL to the page
        """
        return self.reset_password_url

    def is_browser_on_page(self):
        """
        :return: True if reset password form is present
        """
        return self.q(css='#passwordreset-form').present

    def reset_password(self, new_password):
        """
        Reset the password
        :param new_password:
        """
        self.q(css='#new_password1').fill(new_password)
        self.q(css='#new_password2').fill(new_password)
        self.q(css='.action.action-primary.action-update.js-reset').click()
        ResetPasswordComplete(self.browser).wait_for_page()


class ResetPasswordComplete(PageObject):
    """
    Reset password completion
    """

    url = URL_WITH_AUTH + u'password_reset_complete'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if success message is present:
        """
        return self.q(css='.status.submission-success').present

    def go_to_login_page(self):
        """
        Go to login page
        """
        from regression.pages.whitelabel.logistration_page import LoginPage
        self.q(css='.message-copy>a[href="/login"]').click()
        LoginPage(self.browser).wait_for_page()
