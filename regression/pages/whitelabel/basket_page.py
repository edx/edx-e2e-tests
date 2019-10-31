"""
Pages for single course and multi course purchase baskets
"""
from __future__ import absolute_import

import os

import six
from bok_choy.page_object import PageObject

from regression.pages.common.utils import (
    extract_numerical_value_from_price_string,
    fill_input_fields,
    select_value_from_drop_down
)
from regression.pages.whitelabel import ECOM_URL_WITH_AUTH


class BasketPage(PageObject):
    """
    Generic class for E-Commerce basket pages
    """
    url = os.path.join(ECOM_URL_WITH_AUTH, 'basket')

    def is_browser_on_page(self):
        self.wait_for_ajax()
        return self.q(css='#basket-total .price').visible

    def get_error_message_for_invalid_coupon(self):
        """
        Get error message for invalid coupon

        Returns:
            str: error message
        """
        return self.q(css='.alertinner.wicon').text[0]

    @property
    def course_price(self):
        """
        Get the course price

        Returns:
            float: course price
        """
        raw_price = self.q(css='#line-price .price').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    @property
    def total_price(self):
        """
        Get the total price

        Returns:
            float: total price
        """
        raw_price = self.q(css='#basket-total .price').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    @property
    def course_name(self):
        """
        Get course name string

        Returns:
             string: course name
        """
        return self.q(css='.product-name').text[0]

    def logout_from_lms(self):
        """
        Log out from application
        """
        self.q(
            css='.user-menu>.btn.btn-default.dropdown-toggle.'
            'hidden-xs.nav-button'
        ).click()
        self.wait_for_element_visibility(
            '.dropdown-menu',
            'wait for user dropdown to expand'
        )
        self.q(css='.nav-link[href="/logout/"]').click()


class MultiSeatBasketPage(BasketPage):
    """
    Multi Course Basket page
    """


class CyberSourcePage(BasketPage):
    """
    Cybersource payment page
    """
    def set_card_holder_info(self, card_holder_info):
        """
        Fill card holder form using the values passed as arguments

        Arguments:
             card_holder_info(dict): card holder info to fill the form.
        """
        self.wait_for_element_visibility(
            '#card-holder-information',
            'wait for card holder info form'
        )
        elements_and_values = {
            '#id_first_name': card_holder_info['first_name'],
            '#id_last_name': card_holder_info['last_name'],
            '#id_address_line1': card_holder_info['address01'],
            '#id_address_line2': card_holder_info['address02'],
            '#id_city': card_holder_info['city'],
            '#id_postal_code': card_holder_info['postal_code'],
            '#bill_to_email': card_holder_info['email']
        }
        fill_input_fields(self, elements_and_values)
        select_value_from_drop_down(
            self,
            "country",
            card_holder_info['country']
        )
        self.wait_for_element_visibility(
            '#id_state',
            'wait for state drop down'
        )
        select_value_from_drop_down(self, "state", card_holder_info['state'])

    def set_billing_info(self, bill_info):
        """
        Fill billing info using values passed in arguments

        Arguments:
             bill_info(dict): bill info to fill the form.
        """
        self.q(css='#card-number').fill(bill_info['card_number'])
        self.wait_for(
            lambda:
            bill_info['card_type'] in self.q(
                css='.card-type-icon'
            ).attrs('src')[0],
            'wait for visa icon to appear'
        )
        select_names_and_values = {
            "card-expiry-month": bill_info['expiry_month'],
            "card-expiry-year": bill_info['expiry_year']
        }

        for key, val in six.iteritems(select_names_and_values):
            self.wait_for_element_visibility(
                'select[id={}]'.format(key), 'Drop down is visible')
            self.q(
                css='select[id={}] option[value="{}"]'.format(key, val)
            ).click()
            self.wait_for(lambda k=key, v=val: self.q(
                css='select[id={}] option[value="{}"]'.format(k, v)
            ).selected, "Correct value is selected")

        self.q(css='#card-cvn').fill(bill_info['cvn'])

    def click_payment_button(self):
        """
        Click the payment button.
        """
        self.wait_for_element_visibility(
            '#payment-button',
            'Wait for payment button'
        )
        self.q(css='#payment-button').click()


class SingleSeatBasketPage(BasketPage):
    """
    Single course Basket page
    """
    def apply_coupon_code(self, coupon_code):
        """
        Apply coupon code

        Arguments:
             coupon_code(str): The coupon to apply.
        """
        self.wait_for_element_visibility(
            '#voucher_form',
            'Wait for Voucher form to display'
        )
        self.q(css='.code>#id_code').fill(coupon_code)
        self.q(css='.code>.btn.btn-default').click()
        self.wait_for_ajax()

    def is_voucher_applied(self):
        """
        Checks whether voucher is applied.

        Returns:
            bool: True if any voucher is applied on the page:
        """
        return self.q(css='.voucher').present

    def is_offer_applied(self):
        """
        Checks whether offer is applied.

        Returns:
            bool: True if any offer is applied on the page:
        """
        return self.q(css='.offer').present

    @property
    def total_price_after_discount(self):
        """
        Get the total price after discount

        Returns:
            float: price after discount.
        """
        raw_price = self.q(css='#basket-total .price').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    def go_to_receipt_page(self):
        """
        Click on the checkout button to enroll in course for free
        """
        btn_css = '.btn[href="/checkout/free-checkout/"]'
        self.q(css=btn_css).click()
