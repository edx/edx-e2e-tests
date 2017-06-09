"""
Single course Enrollment coupons tests
"""
import random
from itertools import izip
from unittest import skip

from regression.pages.ecommerce.coupon_const import (
    CATALOG_QUERY,
    COUPON_USERS,
    COUPON_TYPE,
    COURSES_CATALOG,
    COURSE_CATALOG_TYPE,
    COURSE_SEAT_TYPES,
    EXPIRED_END_DATE,
    EXPIRED_REDEEM_URL_ERROR,
    FUTURE_CODE_ERROR,
    FUTURE_START_DATE,
    INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET,
    INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL,
    INVALID_DOMAIN_USERS,
    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT,
    ONCE_PER_CUSTOMER_CODE_SAME_USER_REUSE,
    ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT,
    SINGLE_USE_REDEEM_URL_REUSE_ERROR,
    STOCK_RECORD_ID,
    VALID_DOMAIN_USERS,
    VALID_EMAIL_DOMAINS,
    VOUCHER_TYPE
)
from regression.pages.ecommerce.redeem_coupon_page import RedeemCouponPage
from regression.pages.whitelabel.const import (
    PASSWORD,
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.helpers.vouchers import VouchersMixin


class TestDynamicEnrollmentCoupon(VouchersMixin):
    """
    Tests for Single Course Enrollment Coupons
    """

    def setUp(self):
        """
        Prepare setup for running tests
        """
        super(TestDynamicEnrollmentCoupon, self).setUp()
        # Initialize common variables
        course_id, course_info = random.choice(COURSES_CATALOG.items())
        self.course_id = course_id
        self.course_price = course_info['price']
        self.total_price = course_info['price']
        self.course_title = course_info['title']
        # Initialize all page objects
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID)
        # coupon cleanup
        self.addCleanup(self.delete_coupon_after_use)

    @skip('remove after WL-1058 is fixed')
    def test_01_enrollment_once_per_customer_code_max_limit(self):
        """
        Scenario: Dynamic Enrollment Once Per Customer - Code Max Limit: Each
        code can be used up to the number of allowed uses and after that it
        is not usable by any user
        """
        coupon = self.coupon_data(
            COURSE_CATALOG_TYPE['multi'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            catalog_query=CATALOG_QUERY,
            course_seat_types=COURSE_SEAT_TYPES['prof'],
            stock_record_ids=[],
            max_uses=2
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        # Login to application using the existing credentials
        coupon_users = list(COUPON_USERS.values())
        last_user = len(coupon_users) - 1
        for i, coupon_user in enumerate(coupon_users):
            self.login_and_go_to_basket(coupon_user)
            if i != last_user:
                self.addCleanup(
                    self.unenroll_using_api,
                    coupon_user,
                    self.course_id
                )
                self.enroll_using_enrollment_code(coupon_code)
                self.assert_enrollment_and_logout()
            else:
                self.assertEqual(
                    self.error_message_on_invalid_coupon_code(coupon_code),
                    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT
                )

    @skip('remove after WL-1058 is fixed')
    def test_02_apply_enrollment_once_per_customer_redeem_url(self):
        """
        Scenario: Registered Users: Dynamic Enrollment Once Per Customer
        Redeem URL: Each URL can be used up to the number of allowed uses
        and after that it is not usable by any user
        """
        coupon = self.coupon_data(
            COURSE_CATALOG_TYPE['multi'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            catalog_query=CATALOG_QUERY,
            course_seat_types=COURSE_SEAT_TYPES['prof'],
            stock_record_ids=[],
            max_uses=2
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        # Login to application using the existing credentials
        coupon_users = list(COUPON_USERS.values())
        last_user = len(coupon_users) - 1
        for i, coupon_user in enumerate(coupon_users):
            if i != last_user:
                self.addCleanup(
                    self.unenroll_using_api,
                    coupon_user,
                    self.course_id
                )
                self.home.visit()
                self.redeem_multi_course_enrollment_coupon(
                    coupon_code,
                    self.login_page,
                    self.course_title
                )
                self.login_page.authenticate_user(
                    coupon_user,
                    PASSWORD,
                    self.receipt
                )
                self.verify_receipt_info_for_discounted_course()
                self.receipt.go_to_dashboard()
                self.assert_enrollment_and_logout()
            else:
                redeem_coupon = RedeemCouponPage(
                    self.browser,
                    coupon_code
                ).visit()
                self.assertEqual(
                    redeem_coupon.error_message,
                    ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT
                )
