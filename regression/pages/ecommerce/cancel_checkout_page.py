"""
Pages where user is landed after cancelling payment from checkout page
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import ECOMMERCE_URL_WITH_AUTH


class CancelCheckoutPage(PageObject):
    """
    Error page on which user lands when he cancels payment
    """

    url = ECOMMERCE_URL_WITH_AUTH + 'checkout/cancel-checkout'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if error message container is present:
        """
        return self.q(
            css='.container.content-wrapper.receipt-cancel-error'
        ).present

    def get_error_message_header(self):
        """
        Get error message header
        Returns:
            error message header:
        """
        return self.q(
            css='.container.content-wrapper.receipt-cancel-error>h1'
        ).text[0]

    def get_support_email_link(self):
        """
        Get support_email address from error message
        Returns:
            support_email address:
        """
        return self.q(
            css='.container.content-wrapper.receipt-cancel-error>p>a'
        ).attrs('href')[0]
