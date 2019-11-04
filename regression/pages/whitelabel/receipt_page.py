"""
Receipt page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.common.utils import convert_date_format, extract_numerical_value_from_price_string


class ReceiptPage(PageObject):
    """
    Course receipt page
    """

    url = None

    def is_browser_on_page(self):
        return self.q(css='#receipt-container').visible

    @property
    def order_desc(self):
        """
        Get the order description from receipt

        Returns:
            str: Description of the order
        """
        return self.q(css='.course-description>span').text[0]

    @property
    def order_date(self):
        """
        Get the order date from receipt

        Returns:
            str: Date of the order
        """
        date_string = self.q(
            xpath=".//*[@id='receipt-container']//dt[text()='Order Date:']"
                  "/following-sibling::dd"
        ).text[0]
        return convert_date_format(
            date_string,
            '%B %d, %Y',
            '%Y-%m-%d'
        )

    def click_in_nav_to_go_to_dashboard(self):
        """
        Go to user dashboard page by clicking on Go to Dashboard button
        """
        self.q(css='.dashboard-link.nav-link').click()

    @property
    def total_amount(self):
        """
        Get the total amount
        Returns:
            total amount.
        """
        total_amount = self.q(
            css='.order-total:nth-of-type(2)>.price'
        ).text[0]
        return extract_numerical_value_from_price_string(total_amount)

    @property
    def order_amount(self):
        """
        Get the order amount from receipt
        Returns:
            order amount.
        """
        amount = self.q(
            css='.line-price.price'
        ).text[0]
        return extract_numerical_value_from_price_string(amount)

    def get_id_verification_panel_status(self):
        """
        Return the status of the id verification panel.
        """
        return self.q(css=".nav-wizard.row").present
