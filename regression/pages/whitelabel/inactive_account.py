"""
Inactive account page
"""
from regression.tests.helpers.new_page_object import NewPageObject


class InactiveAccount(NewPageObject):
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
