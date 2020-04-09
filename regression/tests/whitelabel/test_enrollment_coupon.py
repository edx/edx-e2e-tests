"""
Single course Enrollment coupons tests
"""
from __future__ import absolute_import

import random
from unittest import skip

from six.moves import range

from regression.pages.studio.utils import get_course_key
from regression.pages.whitelabel import (
    COURSE_NUMBER, COURSE_ORG, COURSE_RUN,
    DEFAULT_COURSE_PRICE
)
from regression.pages.whitelabel.const import PASSWORD
from regression.pages.whitelabel.redeem_coupon_page import RedeemCouponPage
from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.coupon_consts import (
    COUPON_TYPE, COURSE_CATALOG_TYPE, EXPIRED_END_DATE,
    EXPIRED_REDEEM_URL_ERROR, FUTURE_CODE_ERROR, FUTURE_START_DATE,
    INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL, INVALID_DOMAIN_USERS,
    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT, SEAT_TYPE,
    SINGLE_USE_REDEEM_URL_REUSE_ERROR, VALID_EMAIL_DOMAIN, VOUCHER_TYPE
)
from regression.tests.helpers.utils import construct_course_basket_page_url, get_wl_course_info
from regression.tests.whitelabel.voucher_tests_base import VouchersTest


class TestEnrollmentCoupon(VouchersTest):
    """
    Tests for Single Course Enrollment Coupons
    """

    def setUp(self):
        """
        Prepare setup for running tests
        """
        super(TestEnrollmentCoupon, self).setUp()
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

    def test_enrollment_single_use_code(self):
        """
        Scenario: Enrollment Single Use Code: Each code can be used by one
        person successfully
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['single'],
            course_id=self.course_info,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            quantity=2
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_codes = self.coupon.coupon_codes
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        for coupon_code in coupon_codes:
            # Register to application using api
            self.register_using_api(
                construct_course_basket_page_url(self.course_id)
            )
            self.enroll_using_enrollment_code(coupon_code)
            self.assert_enrollment_and_logout_of_ecommerce()

    def test_enrollment_once_per_customer_code_max_limit(self):
        """
        Scenario: Enrollment Once Per Customer - Code Max Limit: Each code can
        be used up to the number of allowed uses and after that it is not
        usable by any user
        """
        maximum_uses = 2
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=self.course_info,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            max_uses=maximum_uses
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        # Login to application using the existing credentials
        for i in range(maximum_uses):
            # Register to application using api
            self.register_using_api(
                construct_course_basket_page_url(self.course_id)
            )
            if i < maximum_uses:
                self.enroll_using_enrollment_code(coupon_code)
                self.assert_enrollment_and_logout_of_ecommerce()
            else:
                self.assertEqual(
                    self.error_message_on_invalid_coupon_code(coupon_code),
                    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT
                )

    def test_enrollment_single_use_code_future(self):
        """
        Scenario: Enrollment Single Use Code: Relevant error message is
        displayed on the use of future coupon
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['single'],
            start_datetime=FUTURE_START_DATE,
            course_id=self.course_info,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id
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
            FUTURE_CODE_ERROR.format(coupon_code)
        )

    def test_apply_enrollment_single_use_redeem_url(self):
        """
        Scenario: Enrollment Single Use Redeem URL: URL cannot be reused
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['single'],
            course_id=self.course_info,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        self.register_using_api()
        self.redeem_single_course_enrollment_coupon(
            coupon_code,
            self.receipt_page
        )
        self.receipt_page.wait_for_page()
        self.verify_receipt_info_for_discounted_course()
        self.receipt_page.click_in_nav_to_go_to_dashboard()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout_of_ecommerce()
        self.register_using_api()
        self.redeem_single_course_enrollment_coupon(
            coupon_code,
            self.redeem_coupon_error_page
        )
        self.assertEqual(
            self.redeem_coupon_error_page.error_message,
            SINGLE_USE_REDEEM_URL_REUSE_ERROR
        )

    @skip("test case modification in progress")
    def test_enrollment_once_per_customer_redeem_url_email_domain(self):
        """
        Scenario: Enrollment Once Per Customer URL: URL can be used only by
        users of valid email domains
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=self.course_info,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            email_domains=VALID_EMAIL_DOMAIN
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        # Login to application using the existing credentials
        invalid_domain_users = list(INVALID_DOMAIN_USERS.values())
        # Verify that coupon url cannot be used for unauthorized email domain
        invalid_domain_user = random.choice(invalid_domain_users)
        self.login_page.visit()
        self.login_user_using_ui(invalid_domain_user, PASSWORD)
        self.redeem_single_course_enrollment_coupon(
            coupon_code,
            self.redeem_coupon_error_page
        )
        self.assertEqual(
            self.redeem_coupon_error_page.error_message,
            INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL
        )

    def test_enrollment_once_per_customer_redeem_url_expired(self):
        """
        Scenario: Enrollment Once Per Customer Redeem URL: Relevant error
        message is displayed on the use of expired redeem url
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            end_datetime=EXPIRED_END_DATE,
            course_id=self.course_info,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id
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
            EXPIRED_REDEEM_URL_ERROR
        )
