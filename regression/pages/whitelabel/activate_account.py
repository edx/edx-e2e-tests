"""
Page for account activation
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject


class ActivateAccount(PageObject):
    """
    Account activation page.
    """

    def __init__(self, browser, activation_url):
        """
        Activate account url has to be set by the test
        """
        super(ActivateAccount, self).__init__(browser)
        self.activate_account_url = activation_url
        self.activation_msg_css = ".account-activation.account" \
                                  "-activation.aa-icon.success"

    @property
    def url(self):
        """
        Construct URL of the page
        """
        return self.activate_account_url

    def is_browser_on_page(self):
        return self.q(css=self.activation_msg_css).present

    @property
    def is_account_activation_complete(self):
        """
        Is account activation complete?
        Returns:
            bool: True if activation complete message is visible:
        """
        return self.q(css=self.activation_msg_css).filter(
            lambda elem: 'You have activated your account.' in elem.text
        ).visible

    def click_dashboard_from_drop_down_menu(self):
        """
        Clicks dashboard from the drop down menu
        """
        self.q(css='.user-name').click()
        self.q(css='.show-user-menu a[href="/dashboard"]').click()
