"""
Pages for single course and multi course purchase baskets
"""
from bok_choy.page_object import PageObject

from regression.pages.common.utils import (
    extract_numerical_value_from_price_string,
    fill_input_fields,
    select_value_from_drop_down
)
from regression.pages.whitelabel.const import ECOMMERCE_URL_WITH_AUTH
from regression.pages.ecommerce.receipt_page import ReceiptPage


class BasketPage(PageObject):
    """
    Generic class for E-Commerce basket pages
    """

    url = ECOMMERCE_URL_WITH_AUTH + 'basket'

    def is_browser_on_page(self):
        """
        Verifies that price is visible
        """
        return self.q(css='#basket-total .price').visible

    @property
    def course_name(self):
        """
        Get course name string
        Returns:
             course name:
        """
        return self.q(css='.product-name').text[0]

    @property
    def course_price(self):
        """
        Get the course price
        Returns:
            course price:
        """
        raw_price = self.q(css='#line-price .price').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    @property
    def total_price(self):
        """
        Get the total price
        Returns:
            total price:
        """
        raw_price = self.q(css='#basket-total .price').text[0]
        return extract_numerical_value_from_price_string(raw_price)


class SingleSeatBasketPage(BasketPage):
    """
    Single course Basket page
    """

    def is_voucher_link_visible(self):
        """
        Is voucher link visible?
        Returns:
             True if link for applying voucher is visible:
        """
        return self.q(css='#voucher_form_link>a').visible

    def is_multi_seat_basket_link_visible(self):
        """
        Is multi seat basket link visible?
        Returns:
            True if link for multi seat basket page is visible:
        """
        link_text = 'Click here to purchase multiple seats in this course'
        return self.q(
            css='.btn.btn-link[href^="/basket"]'
        ).filter(lambda elem: elem.text == link_text).visible

    def apply_coupon_code(self, coupon_code):
        """
        Apply coupon code
        Args:
             coupon_code:
        """
        self.q(css='#voucher_form_link').click()
        self.wait_for_element_visibility(
            '#voucher_form',
            'Wait for Voucher form to display'
        )
        self.q(css='.code>#id_code').fill(coupon_code)
        self.q(css='.code>.btn.btn-default').click()
        self.wait_for_ajax()

    def get_error_message_for_invalid_coupon(self):
        """
        Get error message for invalid coupon
        Returns:
            error message:
        """
        return self.q(css='.alertinner.wicon').text[0]

    @property
    def discount_value(self):
        """
        Get discount amount
        Returns:
            discount amount:
        """
        raw_discount = self.q(css='#line-discount .price').text[0]
        return extract_numerical_value_from_price_string(raw_discount)

    @property
    def total_price_after_discount(self):
        """
        Get the total price after discount
        Returns:
            Total price:
        """
        raw_price = self.q(css='#basket-total .price').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    def is_voucher_applied(self):
        """
        Is voucher applied
        Returns:
            True if any voucher is applied on the page:
        """
        return self.q(css='.voucher').present

    def remove_applied_voucher(self):
        """
        Remove applied voucher
        """
        self.q(css='.remove-voucher').click()
        self.wait_for_element_absence(
            '.voucher',
            'Wait for voucher to disappear'
        )

    def go_to_multi_seat_basket(self):
        """
        Switch to Multi seat basket
        """
        link_text = 'Click here to purchase multiple seats in this course'
        self.q(
            css='.btn.btn-link[href^="/basket"]'
        ).filter(lambda elem: elem.text == link_text).click()
        MultiSeatBasketPage(self.browser).wait_for_page()

    def go_to_receipt_page(self):
        """
        Click on the checkout button to enroll in course for free
        """
        btn_css = '.btn[href="/checkout/free-checkout/"]'
        self.q(css=btn_css).click()
        ReceiptPage(self.browser).wait_for_page()


class MultiSeatBasketPage(BasketPage):
    """
    Multi Course Basket page
    """

    def is_multi_seat_selector_visible(self):
        """
        Is multi seat selector visible?
        Returns:
            True if seat quantity selector is visible:
        """
        return self.q(css='.checkout-quantity.form-group').visible

    @property
    def item_price(self):
        """
        Get the item price
        Returns:
            Item price:
        """
        raw_price = self.q(
            css='.basket-items .course-price-label~span').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    def is_single_seat_basket_link_visible(self):
        """
        Is single seat basket link visible?
        Returns:
            True if link for single seat basket page is visible:
        """
        link_text = 'Click here to just purchase an enrollment for yourself'
        return self.q(
            css='.btn.btn-link[href^="/basket"]'
        ).filter(lambda elem: elem.text == link_text).visible

    @property
    def student_counter_value(self):
        """
        Get student counter value
        Returns:
            student counter value:
        """
        return int(self.q(css='#id_form-0-quantity').attrs('value')[0])

    def increase_student_counter(self, final_val):
        """
        Increase the student counter value by 1 and submit the increment
        Args:
             final_val:
        """
        self.q(css='#id_form-0-quantity').fill(final_val)
        self.q(css='.checkout-quantity .update-button').click()
        self.wait_for_ajax()

    def go_to_single_seat_basket(self):
        """
        Go to single seat basket
        """
        link_text = 'Click here to just purchase an enrollment for yourself'
        self.q(
            css='.btn.btn-link[href^="/basket"]'
        ).filter(lambda elem: elem.text == link_text).click()
        SingleSeatBasketPage(self.browser).wait_for_page()


class CyberSourcePage(BasketPage):
    """
    Cybersource payment page
    """

    def set_card_holder_info(self, card_holder_info):
        """
        Fill card holder form using the values passed from test
        Args:
             card_holder_info:
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
        Provide the billing info using the information from test
        Args:
             bill_info:
        """
        # self.wait_for_element_visibility(
        #     '#billing-information',
        #     'wait for billing info form'
        # )
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
        for key, val in select_names_and_values.iteritems():
            self.wait_for_element_visibility(
                'select[id={}]'.format(key), 'Drop down is visible')
            self.q(
                css='select[id={}] option[value="{}"]'.format(key, val)
            ).click()
            self.wait_for(
                lambda: self.q(
                    css='select[id={}] option[value="{}"]'.
                    format(key, val)
                ).selected, "Correct value is selected"
            )
        self.q(css='#card-cvn').fill(bill_info['cvn'])

    def make_payment(self, target_page):
        """
        Submitting the form will take user to the target page
        Args:
             target_page:
        """
        self.wait_for_element_visibility(
            '#payment-button',
            'Wait for payment button'
        )
        self.q(css='#payment-button').click()
        target_page.wait_for_page()
