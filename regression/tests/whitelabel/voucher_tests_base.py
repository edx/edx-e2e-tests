"""
Common functions for Vouchers
"""
from __future__ import absolute_import

import logging
from datetime import datetime
from bok_choy.browser import save_screenshot

from regression.pages.whitelabel.basket_page import SingleSeatBasketPage
from regression.pages.whitelabel.const import ORG
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.redeem_coupon_page import RedeemCouponErrorPage, RedeemCouponPage
from regression.tests.helpers.api_clients import EcommerceApiClient
from regression.tests.whitelabel.course_enrollment_test import CourseEnrollmentTest

log = logging.getLogger(__name__)


class VouchersTest(CourseEnrollmentTest):
    """
    Base class for tests related to vouchers(coupons)
    """

    def setUp(self):
        super(VouchersTest, self).setUp()
        self.ecommerce_api = EcommerceApiClient()
        # Initialize all objects
        self.home = HomePage(self.browser)
        self.redeem_coupon_error_page = RedeemCouponErrorPage(self.browser)
        self.single_seat_basket = SingleSeatBasketPage(self.browser)
        self.coupon = None

    def enroll_using_discount_code(self, coupon_code):
        """
        Use coupon code to enroll a user in a course.

        Arguments:
            coupon_code(unicode string): The coupon code to use for enrollment.
        """
        self.ecom_cookies = self.browser.get_cookies()
        self.single_seat_basket.apply_coupon_code(coupon_code)
        self.verify_coupon_is_applied_on_basket()
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Verify on receipt page that information like course title,
        # course price, total price
        # order date and billing to is displayed correctly
        self.verify_receipt_info_for_discounted_course()
        self.receipt_page.click_in_nav_to_go_to_dashboard()
        self.dashboard_page.wait_for_page()

    def enroll_using_enrollment_code(self, coupon_code):
        """
        Enroll in the course after enrollment coupon is applied
        Note that for enrollment code we assume a 100% discount
        Arguments:
            coupon_code(unicode string): The coupon code to use for enrollment.
        """
        self.ecom_cookies = self.browser.get_cookies()
        self.single_seat_basket.apply_coupon_code(coupon_code)
        self.verify_after_coupon_is_applied_on_basket()
        self.single_seat_basket.go_to_receipt_page()
        self.receipt_page.wait_for_page()
        # Verify on receipt page that information like course title,
        # course price, total price
        # order date and billing to is displayed correctly
        self.verify_receipt_info_for_discounted_course()
        self.receipt_page.click_in_nav_to_go_to_dashboard()
        self.dashboard_page.wait_for_page()

    def error_message_on_invalid_coupon_code(self, coupon_code):
        """
        Apply the invalid coupon and get error message.

        Arguments:
             coupon_code(unicode string): Coupon code for enrollment.

        Returns:
            str: The error message after applying the coupon.
        """
        self.ecom_cookies = self.browser.get_cookies()
        self.single_seat_basket.apply_coupon_code(coupon_code)
        return self.single_seat_basket.get_error_message_for_invalid_coupon()

    def verify_coupon_is_applied_on_basket(self):
        """
        Verifies that coupon has been applied on the basket page.

        Specifically verify
        i) Coupon code is applied
        ii) Price after coupon application is correct
        """
        self.assertTrue(self.single_seat_basket.is_voucher_applied())
        self.assertEqual(
            self.basket_page.total_price,
            self.coupon.discounted_course_price
        )

    def verify_receipt_info_for_discounted_course(self):
        """
        Verify that info on receipt page is correct.

        Verify
        i) Course title.
        ii) Order date
        """
        self.assertIn(self.course_title, self.receipt_page.order_desc)
        self.assertEqual(
            datetime.utcnow().strftime("%Y-%m-%d"),
            self.receipt_page.order_date
        )

    def redeem_single_course_discount_coupon(self, coupon_code):
        """
        Redeem single course discount coupon.

        Arguments:
            coupon_code: Url of the coupon.
        """
        log.error("Reedem coupon page url: %s", coupon_code)
        redeem_coupon_page = RedeemCouponPage(self.browser, coupon_code)
        redeem_coupon_page.visit()
        redeem_coupon_page.wait_for_course_tile()
        self.verify_course_info_on_coupon_redeem_page(redeem_coupon_page)
        save_screenshot(self.driver, 'zz_' + coupon_code + '_3_redeem_page')
        redeem_coupon_page.click_checkout_button(self.course_id)

    def redeem_single_course_enrollment_coupon(self, coupon_url, target_page):
        """
        Redeem single course enrollment coupon
        Args
            coupon_url: Url of the coupon.
            target_page: Destination page.
        """
        redeem_coupon_page = RedeemCouponPage(self.browser, coupon_url).visit()
        redeem_coupon_page.wait_for_course_tile()
        self.verify_course_info_on_coupon_redeem_page(redeem_coupon_page)
        redeem_coupon_page.redeem_enrollment(target_page)

    def redeem_multi_course_enrollment_coupon(
            self,
            coupon_url,
            target_page,
            course_title):
        """
        Redeem single course enrollment coupon
        Args
            coupon_url: Url of the coupon.
            target_page: Destination page.
            course_title: Title of the course.
        """
        redeem_coupon_page = RedeemCouponPage(self.browser, coupon_url).visit()
        redeem_coupon_page.wait_for_course_tile()
        redeem_coupon_page.set_course_tile_index(course_title)
        self.verify_course_info_on_coupon_redeem_page(redeem_coupon_page)
        redeem_coupon_page.redeem_enrollment(target_page)

    def verify_course_info_on_coupon_redeem_page(self, redeem_coupon_page):
        """
        Verify info on course tile of redeem coupons page.

        Verify
        i) Course Name
        ii) Course Organization
        iii) Discount Value
        iv) Discount type (Absolute or Percentage)
        v) Discounted Price

        Arguments:
             redeem_coupon_page: The redeem coupon page.
        """

        course_info = redeem_coupon_page.get_course_info()
        course_discount_info = redeem_coupon_page.get_course_discount_info()

        self.assertEqual(
            [
                course_info['course_name'],
                course_info['course_org'],
                course_discount_info['benefit_value'],
                course_discount_info['benefit_type'],
                course_discount_info['discounted_price']
            ],
            [
                self.course_title,
                ORG,
                self.coupon.benefit_value,
                self.coupon.benefit_type,
                self.coupon.discounted_course_price
            ]
        )

    def make_payment_after_discount(self, coupon_code=None):
        """
        Payment by active user after discount redeem url was applied.
        """
        log.error("Entered make_payment_after_discount")
        self.verify_info_is_populated_on_basket(
            self.coupon.discounted_course_price
        )
        log.error("Completed verify_info_is_populated_on_basket()")
        save_screenshot(self.driver, 'zz_' + coupon_code + '_5_after_verify_info_is_populated_on_basket')

        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        log.error("Completed otto_payment_using_cyber_source()")
        # Application should take user to the receipt page
        # Verify on receipt page that information like course title,
        # course price, total price
        # order date and billing to are displayed correctly.
        self.verify_receipt_info_for_discounted_course()
        log.error("Completed verify_receipt_info_for_discounted_course()")
        self.receipt_page.click_in_nav_to_go_to_dashboard()
        log.error("Completed receipt_page.click_in_nav_to_go_to_dashboard()")


    def verify_after_coupon_is_applied_on_basket(self):
        """
        After coupon code is applied on basket page, verify Code is applied
        """
        self.assertTrue(self.single_seat_basket.is_voucher_applied())
