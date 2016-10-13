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
        Returns:
                True if error message container is present on the page:
        """
        return self.q(css='.depth.depth-2.message-error').present

    @property
    def error_message_header(self):
        """
        Get error message header
        Returns:
            error message header:
        """
        return self.q(css='.depth.depth-2.message-error>h3').text[0]

    @property
    def dashboard_link_in_error_message(self):
        """
        Get dashboard link from error message
        Returns:
            dashboard link:
        """
        return self.q(
            css='.depth.depth-2.message-error>a'
        ).filter(lambda e: e.text == 'dashboard').attrs('href')

    @property
    def support_email_in_error_message(self):
        """
        Get support_email address from error message
        Returns:
            support_email address:
        """
        return self.q(
            css='.depth.depth-2.message-error>a'
        ).filter(lambda e: 'contact' in e.text).attrs('href')
