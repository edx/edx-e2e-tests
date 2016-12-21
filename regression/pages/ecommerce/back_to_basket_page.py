"""
Pages where user is landed after clicking back button on checkout page
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import ECOMMERCE_URL_WITH_AUTH


class BackToBasketPage(PageObject):
    """
    Error page when user uses back button from payment page
    """

    url = ECOMMERCE_URL_WITH_AUTH + 'basket'

    def is_browser_on_page(self):
        """
        Verifies that error message container is present on the page
        """
        return self.q(css='.depth.depth-2.message-error-content').present

    @property
    def error_message_header(self):
        """
        Get error message header
        Returns:
            error message header:
        """
        return self.q(css='.depth.depth-2.message-error-content>h3').text[0]

    def get_dashboard_link(self):
        """
        Get dashboard link from error message
        Returns:
            dashboard link:
        """
        return self.q(
            css='.depth.depth-2.message-error-content>a'
        ).filter(lambda e: e.text == 'dashboard').attrs('href')

    def get_contact_link(self):
        """
        Get contact link from error message
        Returns:
            support_email address:
        """
        return self.q(
            css='.depth.depth-2.message-error-content>a'
        ).filter(lambda e: 'contact' in e.text ).attrs('href')[0]
