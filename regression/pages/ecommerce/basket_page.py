"""
Pages for single course and multi course purchase baskets
"""
from bok_choy.page_object import PageObject

from regression.pages.common.utils import (
    extract_numerical_value_from_price_string
)
from regression.pages.ecommerce.cybersource_page import CyberSourcePage
from regression.pages.whitelabel.const import (
    DEFAULT_TIMEOUT,
    ECOMMERCE_URL_WITH_AUTH
)
from regression.pages.whitelabel.receipt_page import ReceiptPage


class BasketPage(PageObject):
    """
    Generic class for E-Commerce basket pages
    """

    url = ECOMMERCE_URL_WITH_AUTH + 'basket'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if total price is visible on the page:
        """
        return self.q(css='#basket_totals').visible

    @property
    def course_name(self):
        """
        Get course name string
        Returns:
             course name:
        """
        return self.q(css='.course_name').text[0]

    @property
    def course_price(self):
        """
        Get the course price
        Returns:
            course price:
        """
        raw_price = self.q(css='.price').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    @property
    def total_price(self):
        """
        Get the total price
        Returns:
            total price:
        """
        raw_price = self.q(css='#basket_totals').text[0]
        return extract_numerical_value_from_price_string(raw_price)

    def go_to_cybersource_page(self):
        """
        Click on the cybersource payment button to start the billing process
        """
        self.q(css='#cybersource').click()
        CyberSourcePage(self.browser).wait_for_page()


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
        self.q(css='#voucher_form_link>a').click()
        self.wait_for_element_visibility(
            '#voucher_form',
            'Wait for Voucher form to display'
        )
        self.q(css='.code>#id_code').fill(coupon_code)
        self.q(css='.code>.btn.btn-default').click()
        self.wait_for_ajax()

    @property
    def error_message_for_invalid_coupon(self):
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
        raw_discount = self.q(css='.benefit').text[0]
        return extract_numerical_value_from_price_string(raw_discount)

    @property
    def discounted_amount(self):
        """
        Get discounted price
        Returns:
            discounted price:
        """
        raw_discounted_price = self.q(css='.price.discounted').text[0]
        return extract_numerical_value_from_price_string(raw_discounted_price)

    @property
    def total_price_after_discount(self):
        """
        Get the total price after discount
        :return: Total price
        """
        raw_price = self.q(css='#basket_totals').text[0]
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
        for val in range(1, final_val):
            self.q(css='.checkout-quantity button>.fa.fa-caret-up').click()
            self.wait_for(
                lambda x=val:
                self.student_counter_value == x + 1,
                'Increment is successful',
                timeout=DEFAULT_TIMEOUT
            )
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
