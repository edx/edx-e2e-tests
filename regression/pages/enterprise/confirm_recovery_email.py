"""
Page for Secondary Email activation
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject


class ConfirmRecoveryEmail(PageObject):
    """
    Secondary Email activation page.
    """

    def __init__(self, browser, recovery_email_url):
        """
        Secondary Email account url has to be set by the test
        """
        super(ConfirmRecoveryEmail, self).__init__(browser)
        self.recovery_email_url = recovery_email_url
        self.activation_msg_css = ".message .valid"

    @property
    def url(self):
        """
        Construct URL of the page
        """
        return self.recovery_email_url

    def is_browser_on_page(self):
        return self.q(css=self.activation_msg_css).present

    @property
    def is_secondary_account_activation_complete(self):
        """
        Is Secondary Email account activation complete?
        Returns:
            bool: True if activation complete message is visible:
        """
        return self.q(css=self.activation_msg_css).filter(
            lambda elem: 'Secondary e-mail change successful!' in elem.text
        ).visible
