"""
Receipt page
"""
from bok_choy.page_object import PageObject

from regression.pages.common.utils import (
    convert_date_format,
    extract_numerical_value_from_price_string
)
# commented due to dependency
#from regression.pages.whitelabel.dashboard_page import DashboardPage


class ReceiptException(Exception):
    """
    Catch failures in receipt page
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class ReceiptPage(PageObject):
    """
    Receipt
    """

    url = None

    def is_browser_on_page(self):
        """
        Verifies that receipt report is present on the page:
        """
        return self.q(css='.container').present

    def is_receipt_displayed(self):
        """
        Verifies that receipt is displayed
        Returns:
            True if receipt is found:
        """
        self.wait_for_element_visibility(
            '#receipt-container',
            'wait for receipt to become visible'
        )

    @property
    def order_num(self):
        """
        Get the order number from receipt
        Returns:
            order number:
        """
        return self.q(css='.order-summary>dl>dd:nth-of-type(1)').text[0]

    @property
    def order_desc(self):
        """
        Get the order description from receipt
        Returns:
            order description:
        """
        return self.q(css='.course-description>span').text[0]

    @property
    def order_date(self):
        """
        Get the order date from receipt
        Raises:
            order date:
        """
        date_string = self.q(
            xpath=".//*[@id='receipt-container']//dt[text()='Order Date:']"
                  "/following-sibling::dd"
        ).text[0]
        return convert_date_format(
            date_string,
            '%Y-%m-%dT%H:%M:%SZ',
            # '%B %d, %Y',
            '%Y-%m-%d'
        )

    @property
    def order_amount(self):
        """
        Get the order amount from receipt
        Returns:
            order amount:
        """
        amount = self.q(css='.line-price.price').text[0]
        return extract_numerical_value_from_price_string(amount)

    @property
    def total_amount(self):
        """
        Get the total amount
        Returns:
            total amount:
        """
        total_amount = self.q(css='.order-total:nth-of-type(2)>.price').text[0]
        return extract_numerical_value_from_price_string(total_amount)

    @property
    def billed_to(self):
        """
        Get the information about the person to whom it is billed
        Returns:
            billed_to_info:
        """
        return self.q(css='.confirm-message>a').text[0]

    def go_to_dashboard(self):
        """
        Go to user dashboard page by clicking on Go to Dashboard button
        """
        self.q(css='.dashboard-link.nav-link').click()
        # commented due to dependency
        # DashboardPage(self.browser).wait_for_page()
