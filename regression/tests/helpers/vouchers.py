"""
Common functions for Vouchers
"""
from datetime import datetime
import uuid

from regression.pages.common.api_clients import EcommerceApiClient
from regression.pages.ecommerce.basket_page import SingleSeatBasketPage
from regression.pages.ecommerce.redeem_coupon_page import (
    RedeemCouponPage,
    RedeemCouponErrorPage
)
from regression.pages.ecommerce.coupon_const import (
    BENEFIT_TYPE,
    COUPON_TYPE,
    DEFAULT_END_DATE,
    DEFAULT_START_DATE
)
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.const import ORG

from regression.tests.helpers.voucher_creation import VoucherCreation
from regression.tests.helpers.course_enrollment import CourseEnrollmentMixin


class VouchersMixin(CourseEnrollmentMixin):
    """
    Mixin class for Vouchers
    """

    def setUp(self):
        """
        Setup Voucher Mixin
        """
        super(VouchersMixin, self).setUp()
        self.ecommerce_api = EcommerceApiClient()
        # Initialize all objects
        self.home = HomePage(self.browser)
        self.redeem_coupon_error_page = RedeemCouponErrorPage(self.browser)
        self.single_seat_basket = SingleSeatBasketPage(self.browser)
        self.coupon_id = ''

    def coupon_data(self, catalog_type, coupon_type, voucher_type, **kwargs):
        """
        Return dictionary of values which will be used for filling coupon form
        """
        coupon = {
            "id": "null",
            "title": str(uuid.uuid4().node),
            "catalog_type": catalog_type,
            "code": "",
            "price": "0",
            "quantity": 1,
            "seats": [],
            "course_seats": [],
            "coupon_type": coupon_type,
            "voucher_type": voucher_type,
            "benefit_type": BENEFIT_TYPE['per'],
            "benefit_value": 100,
            "category": {"id": 3, "name": "Affiliate Promotion"},
            "start_datetime": DEFAULT_START_DATE,
            "end_datetime": DEFAULT_END_DATE,
            "client": "Test Client",
            "invoice_type": "Not-Applicable"
        }
        if kwargs:
            coupon.update(kwargs)
        return coupon

    def setup_coupons_using_ui(self, coupon):
        """
        Create and download coupon codes
        Args:
           coupon:
        """
        voucher_creation = VoucherCreation(self.browser)
        voucher_creation.create_coupon(coupon)
        self.coupon_id = voucher_creation.coupon_id
        self.set_discount_details(coupon)
        self.logout_user_from_ecommerce()
        return self.coupon_codes

    def setup_coupons_using_api(self, coupon):
        """
        Create and download coupon codes
        Args:
            coupon:
        """
        self.coupon_id = self.ecommerce_api.create_coupon(coupon)
        self.set_discount_details(coupon)
        return self.coupon_codes

    def set_discount_details(self, coupon):
        """
        Set discount value and type to be used in different calculations
        By default the discount value and type are set to denote an enrollment
        coupon
        Args:
            coupon:
        """
        self.benefit_value = 100
        self.benefit_type = BENEFIT_TYPE['per']
        if coupon['coupon_type'] == COUPON_TYPE['disc']:
            self.benefit_type = coupon['benefit_type']
            self.benefit_value = coupon['benefit_value']

    @property
    def discounted_price(self):
        """
        Perform calculation for discounted amount for Absolute discount
        Returns:
            discounted price:
        """
        if self.benefit_type == BENEFIT_TYPE['abs']:
            return self.course_price - float(self.benefit_value)
        else:
            return self.course_price - \
                (self.course_price * float(self.benefit_value)) / 100

    def enroll_using_discount_code(self, coupon_code):
        """
        Enroll in the course after coupon is applied
        Args:
            coupon_code:
        """
        self.single_seat_basket.apply_coupon_code(coupon_code)
        self.verify_after_coupon_is_applied_on_basket()
        # Go to next page to make the payment
        self.basket.go_to_cybersource_page()
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Verify on receipt page that information like course title,
        # course price, total price
        # order date and billing to is displayed correctly
        self.verify_receipt_info_for_discounted_course()
        self.receipt.go_to_dashboard()

    def enroll_using_enrollment_code(self, coupon_code):
        """
        Enroll in the course after enrollment coupon is applied
        Note that for enrollment code we assume a 100% discount
        Args:
            coupon_code:
        """
        self.single_seat_basket.apply_coupon_code(coupon_code)
        self.verify_after_coupon_is_applied_on_basket()
        self.single_seat_basket.go_to_receipt_page()
        # Verify on receipt page that information like course title,
        # course price, total price
        # order date and billing to is displayed correctly
        self.verify_receipt_info_for_discounted_course()
        self.receipt.go_to_dashboard()

    def redeem_single_course_discount_coupon(self, coupon_url, target_page):
        """
        Redeem single course discount coupon
        Args
            coupon_url:
            target_page:
        """
        redeem_coupon = RedeemCouponPage(self.browser, coupon_url).visit()
        redeem_coupon.wait_for_course_tile()
        self.verify_course_info_on_coupon_redeem_page(redeem_coupon)
        redeem_coupon.checkout_discount_coupon(self.course_id, target_page)

    def redeem_single_course_enrollment_coupon(self, coupon_url, target_page):
        """
        Redeem single course enrollment coupon
        Args
            coupon_url:
            target_page:
        """
        redeem_coupon = RedeemCouponPage(self.browser, coupon_url).visit()
        redeem_coupon.wait_for_course_tile()
        self.verify_course_info_on_coupon_redeem_page(redeem_coupon)
        redeem_coupon.redeem_enrollment(target_page)

    def redeem_multi_course_enrollment_coupon(
            self,
            coupon_url,
            target_page,
            course_title
        ):
        """
        Redeem single course enrollment coupon
        Args
            coupon_url:
            target_page:
            course_title:
        """
        redeem_coupon = RedeemCouponPage(self.browser, coupon_url).visit()
        redeem_coupon.wait_for_course_tile()
        redeem_coupon.set_course_tile_index(course_title)
        self.verify_course_info_on_coupon_redeem_page(redeem_coupon)
        redeem_coupon.redeem_enrollment(target_page)

    def use_discount_redeem_url(self):
        """
        Payment by active user after discount redeem url was applied
        """
        self.verify_info_is_populated_on_basket()
        self.basket.go_to_cybersource_page()
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Application should take user to the receipt page
        # Verify on receipt page that information like course title,
        # course price, total price
        # order date and billing to is displayed correctly
        self.verify_receipt_info_for_discounted_course()
        self.receipt.go_to_dashboard()

    def error_message_on_invalid_coupon_code(self, coupon_code):
        """
        Apply the invalid coupon
        Args:
             coupon_code:
        """
        self.single_seat_basket.apply_coupon_code(coupon_code)
        return self.single_seat_basket.error_message_for_invalid_coupon

    def verify_after_coupon_is_applied_on_basket(self):
        """
        After coupon code is applied on basket page, verify:
        i) Code is applied
        ii) Discount value is correct
        iii) Price after coupon application is correct
        """
        self.assertTrue(self.single_seat_basket.is_voucher_applied())
        self.assertEqual(
            self.single_seat_basket.discount_value,
            self.benefit_value
        )
        self.assertEqual(
            self.single_seat_basket.discounted_amount,
            self.discounted_price
        )
        self.assertEqual(self.basket.total_price, self.discounted_price)

    def verify_course_info_on_coupon_redeem_page(self, redeem_coupon):
        """
        Verify following info on course tile on redeem coupons page:
        i) Course Name
        ii) Course Organization
        iii) Discount Value
        iv) Discount type (Absolute or Percentage)
        v) Discounted Price
        Args:
             redeem_coupon:
        """
        self.assertEqual(
            redeem_coupon.course_info['course_name'],
            self.course_title
        )
        self.assertEqual(
            redeem_coupon.course_info['course_org'],
            ORG
        )
        self.assertEqual(
            redeem_coupon.course_discount_info['benefit_value'],
            self.benefit_value
        )
        self.assertEqual(
            redeem_coupon.course_discount_info['benefit_type'],
            self.benefit_type
        )
        self.assertEqual(
            redeem_coupon.course_discount_info['discounted_price'],
            self.discounted_price
        )

    def verify_info_is_populated_on_basket(self):
        """
        After discount redeem url is used verify that following information is
        displayed correctly
        on basket page:
        i) Coupon is applied
        ii) Discount Value
        iii) Discounted amount
        """
        self.assertTrue(self.single_seat_basket.is_voucher_applied())
        self.assertEqual(
            self.single_seat_basket.discount_value,
            self.benefit_value
        )
        self.assertEqual(
            self.single_seat_basket.discounted_amount,
            self.discounted_price
        )

    def verify_receipt_info_for_discounted_course(self):
        """
        Verify that Course title on receipt page is correct
        Verify that Course price on receipt page is correct
        Verify that total price on receipt page is correct
        Verify that Order date on receipt page is correct
        """
        self.assertTrue(self.receipt.is_receipt_displayed())
        self.assertIn(self.course_title, self.receipt.order_desc)
        self.assertEqual(
            datetime.utcnow().strftime("%Y-%m-%d"),
            self.receipt.order_date
        )
        self.assertEqual(self.receipt.order_amount, self.discounted_price)
        self.assertEqual(self.receipt.total_amount, self.discounted_price)

    def run_full_cleanup(self):
        """
        This is cleanup for coupons which deletes coupons and in case a test
        fails in midway it ue-enrolls student from the course or remove a
        coupon from basket page depending on the current position
        """
        self.delete_coupon_after_use()
        if self.full_cleanup:
            if self.basket.is_browser_on_page() or \
                    self.cyber_source.is_browser_on_page():
                self.remove_voucher_from_basket()
            else:
                self.unenroll_using_ui()

    def remove_voucher_from_basket(self):
        """
        This function removes an already applied voucher from the basket
        """
        if not self.basket.is_browser_on_page():
            self.basket.visit()
        if self.single_seat_basket.is_voucher_applied():
            self.single_seat_basket.remove_applied_voucher()

    @property
    def coupon_codes(self):
        """
        Get coupon codes from coupon report
        """

        return self.ecommerce_api.get_coupon_codes(self.coupon_id)

    def delete_coupon_after_use(self):
        """
        Delete coupon using api
        """
        self.ecommerce_api.delete_coupon(self.coupon_id)
