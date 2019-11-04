"""
Inactive account page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject


class InactiveAccount(PageObject):
    """
    Inactive Account
    """

    url = None

    def is_browser_on_page(self):
        return self.q(css='.activate').visible

    def is_activation_message_present(self):
        """
        Is activation message present?

        Returns:
            bool: True if activation message is visible:
        """
        return self.q(css='.activate-info').visible
