"""
Single course Discount coupons tests
"""
from __future__ import absolute_import

import random
import uuid
from unittest import skip, skipIf

from regression.pages.studio.utils import get_course_key
from regression.pages.whitelabel import (
    COURSE_NUMBER, COURSE_ORG, COURSE_RUN,
    DEFAULT_COURSE_PRICE, TEST_ENV
)
from regression.pages.whitelabel.const import PASSWORD
from regression.pages.whitelabel.redeem_coupon_page import RedeemCouponPage
from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.coupon_consts import (
    BENEFIT_TYPE, BENEFIT_VALUE, COUPON_TYPE, COURSE_CATALOG_TYPE,
    EXPIRED_CODE_ERROR, EXPIRED_END_DATE, FUTURE_REDEEM_URL_ERROR,
    FUTURE_START_DATE, INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET,
    INVALID_DOMAIN_USERS, ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE,
    SEAT_TYPE, SINGLE_USE_CODE_REUSE_ERROR, VALID_EMAIL_DOMAIN, VOUCHER_TYPE
)
from regression.tests.helpers.utils import (
    construct_course_basket_page_url,
    get_white_label_registration_fields,
    get_wl_course_info
)
from regression.tests.whitelabel.voucher_tests_base import VouchersTest


class TestDiscountCoupon(VouchersTest):
    """
    Tests for Single Course Discount Coupons
    """
    def setUp(self):
        super(TestDiscountCoupon, self).setUp()
        # Initialize common variables
        self.course_info = get_wl_course_info(
            org=COURSE_ORG,
            num=COURSE_NUMBER,
            run=COURSE_RUN
        )
        self.course_id = str(get_course_key(self.course_info))
        self.course_title = self.course_info["display_name"]
        self.course_price = DEFAULT_COURSE_PRICE
        self.total_price = DEFAULT_COURSE_PRICE
        self.stock_record_id = self.ecommerce_api.get_stock_record_id(
            self.course_id,
            self.course_title
        )

    def test_discount_single_use_percentage_code(self):
        """
        Scenario: Discount Single Use Percentage Code: Code cannot be reused
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['single'],
            course_id=self.course_id,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            benefit_type=BENEFIT_TYPE['per'],
            benefit_value=BENEFIT_VALUE['per']
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        # Register to application using api
        self.register_using_api(
            construct_course_basket_page_url(self.course_id)
        )
        self.enroll_using_discount_code(coupon_code)
        self.assert_enrollment_and_logout_of_ecommerce()
        self.register_using_api(
            construct_course_basket_page_url(self.course_id)
        )
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            SINGLE_USE_CODE_REUSE_ERROR.format(coupon_code)
        )

    @skip('skipped as coupon creation is behaving erratically')
    def test_discount_once_per_customer_fixed_code_email_domain(self):
        """
        Scenario: Discount Once Per Customer Fixed Code: Code cannot be used
        by users of invalid email domains
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=self.course_id,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
            email_domains=VALID_EMAIL_DOMAIN
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        # Login to application using the invalid domain user credentials
        invalid_domain_users = list(INVALID_DOMAIN_USERS.values())
        # Verify that coupon code cannot be added for unauthorized email domain
        invalid_domain_user = random.choice(invalid_domain_users)
        self.login_page.visit()
        self.login_user_using_ui(invalid_domain_user, PASSWORD)
        self.go_to_basket()
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET
        )

    def test_discount_single_use_fixed_code_expired(self):
        """
        Scenario: Discount Single Use Fixed Code: Relevant error message is
        displayed on the use of Expired coupon
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['single'],
            end_datetime=EXPIRED_END_DATE,
            course_id=self.course_id,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed']
        )

        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        # Register to application using api
        self.register_using_api(
            construct_course_basket_page_url(self.course_id)
        )
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            EXPIRED_CODE_ERROR.format(coupon_code)
        )

    def test_discount_single_use_fixed_redeem_url(self):
        """
        Scenario: Existing Users - Discount Single Use Fixed Redeem URL: Each
        redeem url can be used by one person successfully
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['single'],
            course_id=self.course_id,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
            quantity=2
        )

        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_codes = self.coupon.coupon_codes
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        for coupon_code in coupon_codes:
            # Register to application using api
            self.register_using_api()
            self.redeem_single_course_discount_coupon(coupon_code)
            self.basket_page.wait_for_page()
            self.make_payment_after_discount()
            self.dashboard_page.wait_for_page()
            self.assert_enrollment_and_logout_of_ecommerce()

    @skipIf(TEST_ENV == "stage", "skip tests on stage")
    def test_discount_once_per_customer_percentage_redeem_url(self):
        """
        Scenario: Inactive Users - Discount Once Per Customer Percentage
        Redeem URL: URL cannot be used twice by he same user
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=self.course_id,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            benefit_type=BENEFIT_TYPE['per'],
            benefit_value=BENEFIT_VALUE['per']
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        self.home.visit()
        self.redeem_single_course_discount_coupon(coupon_code)
        self.login_page.wait_for_page()
        self.login_page.toggle_to_registration_page()
        self.registration_page.wait_for_page()
        user_name = str(uuid.uuid4().node)
        temp_mail = user_name + "@example.com"

        self.registration_page.register_white_label_user(
            get_white_label_registration_fields(
                email=temp_mail,
                username=user_name
            )
        )
        self.single_seat_basket.wait_for_page()
        self.make_payment_after_discount()
        self.assert_course_added_to_dashboard()
        redeem_coupon = RedeemCouponPage(self.browser, coupon_code).visit()
        self.assertEqual(
            redeem_coupon.error_message,
            ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE
        )

    def test_discount_once_per_customer_fixed_redeem_url_future(self):
        """
        Scenario: Discount Once Per Customer Fixed Redeem URL: Relevant error
        message is displayed on the use of future redeem url
        """

        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['once_per_cust'],
            start_datetime=FUTURE_START_DATE,
            course_id=self.course_id,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
            max_uses=2
        )

        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        # Register to application using api
        self.register_using_api()
        redeem_coupon = RedeemCouponPage(self.browser, coupon_code).visit()
        self.assertEqual(
            redeem_coupon.error_message,
            FUTURE_REDEEM_URL_ERROR
        )
