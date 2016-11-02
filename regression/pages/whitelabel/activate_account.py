"""
Page for account activation
"""

from bok_choy.page_object import PageObject


class ActivateAccount(PageObject):
    """
    Activate Account Class
    """

    def __init__(self, browser, activation_url):
        """
        Activate account url has to be set by the test
        """
        super(ActivateAccount, self).__init__(browser)
        self.activate_account_url = activation_url

    @property
    def url(self):
        """
        Construct a URL to the page
        """
        return self.activate_account_url

    def is_browser_on_page(self):
        return self.q(css='.message>.valid').present

    def is_account_activation_complete(self):
        """
        Is account activation complet?
        Returns:
            True if activation complete message is visible:
        """
        return self.q(
            css='.message>.valid'
        ).filter(lambda elem: elem.text == 'Activation Complete!').visible

    def go_to_dashboard_after_activation(self):
        """
        Go to dashboard after activation is complete
        """
        from regression.pages.whitelabel.dashboard_page import DashboardPage
        self.q(css='.message>p>a[href="/dashboard"]').click()
        DashboardPage(self.browser).wait_for_page()
