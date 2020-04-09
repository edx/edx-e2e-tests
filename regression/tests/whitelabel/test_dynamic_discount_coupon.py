"""
Multi course Discount coupons tests
"""
from __future__ import absolute_import

import random
from unittest import skip

from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.coupon_consts import (
    BENEFIT_TYPE, BENEFIT_VALUE, CATALOG_QUERY, COUPON_TYPE,
    COURSE_CATALOG_TYPE, COURSE_SEAT_TYPES, COURSES_CATALOG,
    SINGLE_USE_CODE_REUSE_ERROR, VOUCHER_TYPE
)
from regression.tests.helpers.utils import construct_course_basket_page_url
from regression.tests.whitelabel.voucher_tests_base import VouchersTest


class TestDynamicDiscountCoupon(VouchersTest):
    """
    Tests for Single Course Discount Coupons
    """

    def setUp(self):
        """
        Prepare setup for running tests
        """
        super(TestDynamicDiscountCoupon, self).setUp()
        # Initialize common variables
        course_id, course_info = random.choice(list(COURSES_CATALOG.items()))
        self.course_id = course_id
        self.course_price = course_info['price']
        self.total_price = course_info['price']
        self.course_title = course_info['title']
        # Initialize all page objects
        self.course_about = CourseAboutPage(self.browser, self.course_id)

    @skip("Need to rewrite tests for sandbox")
    def test_discount_single_use_percentage_code(self):
        """
        Scenario: Dynamic Discount Single Use Percentage Code: Code cannot
        be reused
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['multi'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['single'],
            catalog_query=CATALOG_QUERY,
            stock_record_ids=[],
            course_seat_types=COURSE_SEAT_TYPES['prof'],
            benefit_type=BENEFIT_TYPE['per'],
            benefit_value=BENEFIT_VALUE['per']
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Login to application using the existing credentials
        self.login_page.visit()
        # Register to application using api
        self.register_using_api(
            construct_course_basket_page_url(self.course_id)
        )
        self.enroll_using_discount_code(coupon_code)
        self.assert_enrollment_and_logout_of_ecommerce()
        # Register to application using api
        self.register_using_api(
            construct_course_basket_page_url(self.course_id)
        )
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            SINGLE_USE_CODE_REUSE_ERROR.format(coupon_code)
        )
