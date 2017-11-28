"""
Single course Enrollment coupons tests
"""
import random

from regression.pages.whitelabel.const import (
    PASSWORD,
    PROF_COURSE_ID,
    PROF_COURSE_PRICE,
    PROF_COURSE_TITLE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.redeem_coupon_page import RedeemCouponPage
from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.coupon_consts import (
    COUPON_TYPE,
    COUPON_USERS,
    COURSE_CATALOG_TYPE,
    EXPIRED_END_DATE,
    EXPIRED_REDEEM_URL_ERROR,
    FUTURE_CODE_ERROR,
    FUTURE_START_DATE,
    INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL,
    INVALID_DOMAIN_USERS,
    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT,
    SEAT_TYPE,
    SINGLE_USE_REDEEM_URL_REUSE_ERROR,
    STOCK_RECORD_ID,
    VALID_EMAIL_DOMAIN,
    VOUCHER_TYPE
)
from regression.tests.helpers.utils import construct_course_basket_page_url
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
        # Initialize all page objects
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID)
        # Initialize common variables
        self.course_id = PROF_COURSE_ID
        self.course_price = PROF_COURSE_PRICE
        self.course_title = PROF_COURSE_TITLE
        self.total_price = PROF_COURSE_PRICE

    def test_enrollment_single_use_code(self):
        """
        Scenario: Enrollment Single Use Code: Each code can be used by one
        person successfully
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['single'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            quantity=2
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_codes = self.coupon.coupon_codes
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        for coupon_code in coupon_codes:
            # Register to application using api
            self.register_using_api(
                construct_course_basket_page_url(PROF_COURSE_ID)
            )
            self.enroll_using_enrollment_code(coupon_code)
            self.assert_enrollment_and_logout()

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
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
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
                construct_course_basket_page_url(PROF_COURSE_ID)
            )
            if i < maximum_uses:
                self.enroll_using_enrollment_code(coupon_code)
                self.assert_enrollment_and_logout()
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
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        # Login to application using the existing credentials
        self.login_page.visit()
        self.login_user_using_ui(COUPON_USERS['coupon_user_01'], PASSWORD)
        self.go_to_basket()
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
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID
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
        self.ecom_cookies = self.browser.get_cookies()
        self.receipt_page.wait_for_page()
        self.verify_receipt_info_for_discounted_course()
        self.receipt_page.click_in_nav_to_go_to_dashboard()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout()
        self.register_using_api()
        self.redeem_single_course_enrollment_coupon(
            coupon_code,
            self.redeem_coupon_error_page
        )
        self.assertEqual(
            self.redeem_coupon_error_page.error_message,
            SINGLE_USE_REDEEM_URL_REUSE_ERROR
        )

    def test_enrollment_once_per_customer_redeem_url_email_domain(self):
        """
        Scenario: Enrollment Once Per Customer URL: URL can be used only by
        users of valid email domains
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
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
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Delete coupon after test
        self.addCleanup(self.coupon.delete_coupon)
        self.login_page.visit()
        self.login_user_using_ui(COUPON_USERS['coupon_user_01'], PASSWORD)
        self.go_to_basket()
        redeem_coupon = RedeemCouponPage(self.browser, coupon_code).visit()
        self.assertEqual(
            redeem_coupon.error_message,
            EXPIRED_REDEEM_URL_ERROR
        )
