"""
Multi course Discount coupons tests
"""
import random
from unittest import skip

from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.coupon_consts import (
    BENEFIT_TYPE,
    BENEFIT_VALUE,
    CATALOG_QUERY,
    COURSES_CATALOG,
    COUPON_USERS,
    COUPON_TYPE,
    COURSE_CATALOG_TYPE,
    COURSE_SEAT_TYPES,
    SINGLE_USE_CODE_REUSE_ERROR,
    VOUCHER_TYPE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
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
        course_id, course_info = random.choice(COURSES_CATALOG.items())
        self.course_id = course_id
        self.course_price = course_info['price']
        self.total_price = course_info['price']
        self.course_title = course_info['title']
        # Initialize all page objects
        self.course_about = CourseAboutPage(self.browser, self.course_id)

    @skip
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
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_01'])
        self.addCleanup(
            self.unenroll_using_api,
            COUPON_USERS['coupon_user_01'],
            self.course_id
        )
        self.enroll_using_discount_code(coupon_code)
        self.assert_enrollment_and_logout()
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_02'])
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            SINGLE_USE_CODE_REUSE_ERROR.format(coupon_code)
        )
