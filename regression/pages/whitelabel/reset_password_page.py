"""
Reset Password page
"""
from regression.tests.helpers.new_page_object import NewPageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH


class ResetPassword(NewPageObject):
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
        return self.q(css='#passwordreset-form').present

    def reset_password(self, new_password, submit=True):
        """
        Reset the password
        Arguments:
            new_password(str): New password to be set.
            submit(bool): Whether to submit the form or not.
        """
        self.q(css='#new_password1').fill(new_password)
        self.q(css='#new_password2').fill(new_password)
        if submit:
            self.q(css='.action.action-primary.action-update.js-reset').click()


class ResetPasswordComplete(NewPageObject):
    """
    Reset password completion page
    """

    url = URL_WITH_AUTH + u'password_reset_complete'

    def is_browser_on_page(self):
        return self.q(css='.status.submission-success').present

    def click_login_button(self):
        """
        Clicks login button
        """
        self.q(css='.message-copy>a[href^="/login"]').click()
