"""
Multi course Discount coupons tests
"""
import random
from itertools import izip
from unittest import skip

from regression.pages.ecommerce.coupon_const import (
    BENEFIT_TYPE,
    BENEFIT_VALUE,
    CATALOG_QUERY,
    COURSES_CATALOG,
    COUPON_USERS,
    COUPON_TYPE,
    COURSE_CATALOG_TYPE,
    COURSE_SEAT_TYPES,
    EXPIRED_CODE_ERROR,
    EXPIRED_END_DATE,
    FUTURE_START_DATE,
    FUTURE_REDEEM_URL_ERROR,
    INACTIVE_ACCOUNT_ERROR_MESSAGE,
    INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET,
    INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL,
    INVALID_DOMAIN_USERS,
    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT,
    ONCE_PER_CUSTOMER_CODE_SAME_USER_REUSE,
    ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT,
    ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE,
    SINGLE_USE_CODE_REUSE_ERROR,
    SINGLE_USE_REDEEM_URL_REUSE_ERROR,
    STOCK_RECORD_ID,
    VALID_DOMAIN_USERS,
    VALID_EMAIL_DOMAINS,
    VOUCHER_TYPE
)
from regression.pages.ecommerce.redeem_coupon_page import RedeemCouponPage
from regression.pages.whitelabel.const import (
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.helpers.vouchers import VouchersMixin


class TestDynamicDiscountCoupon(VouchersMixin):
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
        # coupon cleanup
        self.addCleanup(self.delete_coupon_after_use)

    def test_01_discount_single_use_percentage_code(self):
        """
        Scenario: Discount Single Use Percentage Code: Code cannot be reused
        """
        coupon = self.coupon_data(
            COURSE_CATALOG_TYPE['multi'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['single'],
            catalog_query=CATALOG_QUERY,
            stock_record_ids=[],
            course_seat_types=COURSE_SEAT_TYPES['prof'],
            benefit_type=BENEFIT_TYPE['per'],
            benefit_value=BENEFIT_VALUE['per']
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
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
