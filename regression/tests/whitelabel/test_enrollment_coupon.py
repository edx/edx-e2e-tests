"""
Single course Enrollment coupons tests
"""
import random
import uuid
from itertools import izip

from regression.tests.helpers.coupon_consts import (
    COUPON_USERS,
    COUPON_TYPE,
    COURSE_CATALOG_TYPE,
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
    SEAT_TYPE,
    SINGLE_USE_REDEEM_URL_REUSE_ERROR,
    STOCK_RECORD_ID,
    VALID_DOMAIN_USERS,
    VALID_EMAIL_DOMAINS,
    VOUCHER_TYPE
)
from regression.pages.whitelabel.redeem_coupon_page import RedeemCouponPage
from regression.tests.helpers.coupon import Coupon
from regression.pages.whitelabel.const import (
    PASSWORD,
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.whitelabel.voucher_tests_base import VouchersTest
from regression.tests.helpers.utils import get_white_label_registration_fields
from regression.tests.helpers.api_clients import GuerrillaMailApi
from regression.tests.helpers.utils import activate_account


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
            quantity=3
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_codes = self.coupon.coupon_codes
        coupon_users = list(COUPON_USERS.values())
        # Login to application using the existing credentials
        for coupon_user, coupon_code in izip(coupon_users, coupon_codes):
            self.addCleanup(
                self.unenroll_using_api,
                coupon_user,
                self.course_id
            )
            self.login_and_go_to_basket(coupon_user)
            self.enroll_using_enrollment_code(coupon_code)
            self.assert_enrollment_and_logout()

    def test_enrollment_once_per_customer_code_max_limit(self):
        """
        Scenario: Enrollment Once Per Customer - Code Max Limit: Each code can
        be used up to the number of allowed uses and after that it is not
        usable by any user
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            max_uses=2
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Login to application using the existing credentials
        coupon_users = list(COUPON_USERS.values())
        last_user_index = len(coupon_users) - 1
        for coupon_user_index, coupon_user in enumerate(coupon_users):
            self.login_and_go_to_basket(coupon_user)
            if coupon_user_index != last_user_index:
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

    def test_enrollment_once_per_customer_code_reuse_by_same_user(self):
        """
        Scenario: Enrollment Once Per Customer - Code Reuse: A code cannot
        be used twice by the same user
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            max_uses=2
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
        self.enroll_using_enrollment_code(coupon_code)
        self.assert_enrollment_and_unenroll()
        self.dashboard_page.go_to_find_courses_page()
        self.courses_page.wait_for_page()
        # find the target course and click on it to go to about page
        self.courses_page.go_to_course_about_page(self.course_about)
        # go to single seat basket page
        self.course_about.click_on_single_seat_basket()
        self.single_seat_basket_page.wait_for_page()
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            ONCE_PER_CUSTOMER_CODE_SAME_USER_REUSE
        )

    def test_enrollment_once_per_customer_code_email_domain(self):
        """
        Scenario: Enrollment Once Per Customer Code - Email domains: Code can
        be used only by users of valid email domains
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            email_domains=VALID_EMAIL_DOMAINS,
            max_uses=5
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Login to application using the existing credentials
        valid_domain_users = list(VALID_DOMAIN_USERS.values())
        invalid_domain_users = list(INVALID_DOMAIN_USERS.values())
        # Verify that coupon code cannot be added for unauthorized email domain
        # In each test we are selecting a random user from the invalid domain
        # list to bring down the test run time. Since multiple tests will be
        # running for domain checks, use of random user in all of these will
        # pretty much cover most of the possibilities
        invalid_domain_user = random.choice(invalid_domain_users)
        self.login_and_go_to_basket(invalid_domain_user)
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET
        )
        self.basket_page.logout_from_lms()
        self.home_page.wait_for_page()
        # Verify that coupon code can be added for authorized email domain
        # In each test we are selecting a random user from the valid domain
        # list to bring down the test run time. Since multiple tests will be
        # running for domain checks, use of random user in all of these will
        # pretty much cover most of the possibilities
        valid_domain_user = random.choice(valid_domain_users)
        self.addCleanup(
            self.unenroll_using_api,
            valid_domain_user,
            self.course_id
        )
        self.login_and_go_to_basket(valid_domain_user)
        self.enroll_using_enrollment_code(coupon_code)
        self.assert_enrollment_and_logout()

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
        # Login to application using the existing credentials
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_01'])
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            FUTURE_CODE_ERROR.format(coupon_code)
        )

    def test_apply_enrollment_single_use_redeem_url(self):
        """
        Scenario: Unregistered Users: Enrollment Single Use Redeem URL: URL
        cannot be reused
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
        self.home.visit()
        self.home.go_to_registration_page()
        self.registration_page.wait_for_page()
        user_name = str(uuid.uuid4().node)
        temp_mail = GuerrillaMailApi(user_name)

        self.registration_page.register_white_label_user(
            get_white_label_registration_fields(
                email=temp_mail.user_email,
                password=PASSWORD,
                user_name=temp_mail.user_name
            )
        )
        activate_account(self, temp_mail)
        self.redeem_single_course_enrollment_coupon(
            coupon_code,
            self.receipt_page
        )
        self.receipt_page.wait_for_page()
        self.verify_receipt_info_for_discounted_course()
        self.receipt_page.click_in_nav_to_go_to_dashboard()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout()
        self.login_page.visit()
        self.login_user_using_ui(COUPON_USERS['coupon_user_01'], PASSWORD)
        self.redeem_single_course_enrollment_coupon(
            coupon_code,
            self.redeem_coupon_error_page
        )
        self.assertEqual(
            self.redeem_coupon_error_page.error_message,
            SINGLE_USE_REDEEM_URL_REUSE_ERROR
        )

    def test_apply_enrollment_once_per_customer_redeem_url(self):
        """
        Scenario: Registered Users: Enrollment Once Per Customer Redeem URL:
        Each URL can be used up to the number of allowed uses and after that
        it is not usable by any user
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['enroll'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            max_uses=2
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
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
                self.redeem_single_course_enrollment_coupon(
                    coupon_code, self.login_page)
                self.login_page.authenticate_user(
                    coupon_user,
                    PASSWORD
                )
                self.receipt_page.wait_for_page()
                self.verify_receipt_info_for_discounted_course()
                self.receipt_page.click_in_nav_to_go_to_dashboard()
                self.dashboard_page.wait_for_page()
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
            email_domains=VALID_EMAIL_DOMAINS,
            max_uses=5
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Login to application using the existing credentials
        valid_domain_users = list(VALID_DOMAIN_USERS.values())
        invalid_domain_users = list(INVALID_DOMAIN_USERS.values())
        # Verify that coupon url cannot be used for unauthorized email domain
        # In each test we are selecting a random user from the invalid domain
        # list to bring down the test run time. Since multiple tests will be
        # running for domain checks, use of random user in all of these will
        # pretty much cover most of the possibilities
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
        self.logout_user_from_ecommerce()
        self.home.wait_for_page()
        # Verify that coupon url can be used for authorized email domain
        # In each test we are selecting a random user from the valid domain
        # list to bring down the test run time. Since multiple tests will be
        # running for domain checks, use of random user in all of these will
        # pretty much cover most of the possibilities
        valid_domain_user = random.choice(valid_domain_users)
        self.addCleanup(
            self.unenroll_using_api,
            valid_domain_user,
            self.course_id
        )
        self.login_page.visit()
        self.login_user_using_ui(valid_domain_user, PASSWORD)
        self.redeem_single_course_enrollment_coupon(
            coupon_code,
            self.receipt_page
        )
        self.verify_receipt_info_for_discounted_course()
        self.receipt_page.click_in_nav_to_go_to_dashboard()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout()

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
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_01'])
        redeem_coupon = RedeemCouponPage(self.browser, coupon_code).visit()
        self.assertEqual(
            redeem_coupon.error_message,
            EXPIRED_REDEEM_URL_ERROR
        )
