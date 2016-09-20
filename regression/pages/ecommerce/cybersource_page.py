"""
Cybersource page
"""
from bok_choy.page_object import PageObject

from regression.pages.common.utils import (
    fill_input_fields,
    select_values_from_drop_downs,
    click_checkbox
)
from regression.pages.ecommerce.back_to_basket_page import BackToBasketPage
from regression.pages.ecommerce.cancel_checkout_page import CancelCheckoutPage


class CyberSourcePage(PageObject):
    """
    Cybersource payment page
    """

    url = 'https://testsecureacceptance.cybersource.com/checkout'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if payment button is present:
        """
        return self.q(css='.right.complete.pay_button').present

    def set_billing_info(self, bill_info):
        """
        Fill billing form using the values passed from test
        Args:
             bill_info:
        """
        fill_css_selectors = [
            '#bill_to_forename',
            '#bill_to_surname',
            '#bill_to_address_line1',
            '#bill_to_address_line2',
            '#bill_to_address_city',
            '#bill_to_address_postal_code',
            '#bill_to_email'
        ]
        fill_values = [
            bill_info['first_name'],
            bill_info['last_name'],
            bill_info['address01'],
            bill_info['address02'],
            bill_info['city'],
            bill_info['postal_code'],
            bill_info['email']
        ]
        select_names = [
            "bill_to_address_country",
            "bill_to_address_state_us_ca"
        ]
        select_values = [bill_info['country'], bill_info['state']]
        fill_input_fields(self, fill_css_selectors, fill_values)
        select_values_from_drop_downs(self, select_names, select_values)

    def set_payment_details(self, payment_details):
        """
        Provide the payment details using the information from test
        Args:
             payment_details:
        """
        click_checkbox(self, '#card_type_001')
        fill_css_selectors = ['#card_number', '#card_cvn']
        fill_values = [payment_details['card_number'], payment_details['cvn']]
        fill_input_fields(self, fill_css_selectors, fill_values)
        select_names = ["card_expiry_month", "card_expiry_year"]
        select_values = [
            payment_details['expiry_month'],
            payment_details['expiry_year'],
        ]
        select_values_from_drop_downs(self, select_names, select_values)

    def make_payment(self, target_page):
        """
        Submitting the form will take user to the target page
        Args:
             target_page:
        """
        self.wait_for_element_visibility(
            '.right.complete.pay_button',
            'Wait for payment button'
        )
        self.q(css='.right.complete.pay_button').click()
        target_page.wait_for_page()

    def go_back_to_basket_page(self):
        """
        Go back using browser back button
        Selenium back() function is not very stable so using Javascript
        """
        self.browser.execute_script("window.history.go(-1)")
        BackToBasketPage(self.browser).wait_for_page()

    def cancel_checkout(self):
        """
        Cancel checkout
        """
        dailog_box = '.ui-dialog.ui-widget[style*="display: block"]'
        self.q(css='.left.cancelbutton').click()
        self.wait_for_element_presence(
            dailog_box,
            'wait for dialog box with {display: block}'
        )
        self.q(css=dailog_box + ' .ui-button:nth-of-type(1)').click()
        CancelCheckoutPage(self.browser).wait_for_page()
