"""
Single course Enrollment coupons tests
"""
from __future__ import absolute_import

import random
from unittest import skip

from six.moves import range

from regression.pages.whitelabel.const import PASSWORD
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.redeem_coupon_page import RedeemCouponPage
from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.coupon_consts import (
    CATALOG_QUERY, COUPON_TYPE, COURSE_CATALOG_TYPE, COURSE_SEAT_TYPES,
    COURSES_CATALOG, ONCE_PER_CUSTOMER_CODE_MAX_LIMIT,
    ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT, VOUCHER_TYPE
)
from regression.tests.helpers.utils import construct_course_basket_page_url
from regression.tests.whitelabel.voucher_tests_base import VouchersTest


class TestDynamicEnrollmentCoupon(VouchersTest):
    """
    Tests for Single Course Enrollment Coupons
    """

    def setUp(self):
        """
        Prepare setup for running tests
        """
        super(TestDynamicEnrollmentCoupon, self).setUp()
        # Initialize common variables
        course_id, course_info = random.choice(list(COURSES_CATALOG.items()))
        self.course_id = course_id
        self.course_price = course_info['price']
        self.total_price = course_info['price']
        self.course_title = course_info['title']
        # Initialize all page objects
        self.course_about = CourseAboutPage(self.browser, self.course_id)

    @skip("Need to rewrite tests for sandbox")
    def test_enrollment_once_per_customer_code_max_limit(self):
        """
        Scenario: Dynamic Enrollment Once Per Customer - Code Max Limit: Each
        code can be used up to the number of allowed uses and after that it
        is not usable by any user
        """
        maximum_uses = 2
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['multi'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            catalog_query=CATALOG_QUERY,
            course_seat_types=COURSE_SEAT_TYPES['prof'],
            stock_record_ids=[],
            max_uses=maximum_uses
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        self.addCleanup(self.coupon.delete_coupon)
        coupon_code = self.coupon.coupon_codes[0]
        for i in range(maximum_uses):
            if i < maximum_uses:
                # Register to application using api
                self.register_using_api(
                    construct_course_basket_page_url(self.course_id)
                )
                self.enroll_using_enrollment_code(coupon_code)
                self.assert_enrollment_and_logout_of_ecommerce()
            else:
                # Register to application using api
                self.register_using_api(
                    construct_course_basket_page_url(self.course_id)
                )
                self.assertEqual(
                    self.error_message_on_invalid_coupon_code(coupon_code),
                    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT
                )

    @skip("Need to rewrite tests for sandbox")
    def test_apply_enrollment_once_per_customer_redeem_url(self):
        """
        Scenario: Registered Users: Dynamic Enrollment Once Per Customer
        Redeem URL: Each URL can be used up to the number of allowed uses
        and after that it is not usable by any user
        """
        maximum_uses = 2
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['multi'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            catalog_query=CATALOG_QUERY,
            course_seat_types=COURSE_SEAT_TYPES['prof'],
            stock_record_ids=[],
            max_uses=maximum_uses
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        for i in range(maximum_uses):
            if i < maximum_uses:
                # Register to application using api
                self.register_using_api()
                self.redeem_multi_course_enrollment_coupon(
                    coupon_code,
                    self.login_page,
                    self.course_title
                )
                self.login_page.authenticate_user(
                    "coupon_user",
                    PASSWORD
                )
                self.receipt_page.wait_for_page()
                self.verify_receipt_info_for_discounted_course()
                self.receipt_page.click_in_nav_to_go_to_dashboard()
                self.dashboard_page.wait_for_page()
                self.assert_enrollment_and_logout_of_ecommerce()
            else:
                self.register_using_api()
                redeem_coupon = RedeemCouponPage(
                    self.browser,
                    coupon_code
                ).visit()
                self.assertEqual(
                    redeem_coupon.error_message,
                    ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT
                )
