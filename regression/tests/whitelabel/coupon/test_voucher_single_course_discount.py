"""
Single course Discount coupons tests
"""
import random
from itertools import izip

from regression.pages.common.utils import skip_cleanup_if_test_passed
from regression.pages.ecommerce.coupon_const import (
    ABSOLUTE_BENEFIT_TYPE,
    COUPON_USERS,
    DEFAULT_FIXED_BENEFIT_VALUE,
    DEFAULT_PERCENTAGE_BENEFIT_VALUE,
    DISCOUNT_COUPON_TYPE,
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
    ONCE_PER_CUSTOMER_VOUCHER_TYPE,
    PERCENTAGE_BENEFIT_TYPE,
    SINGLE_COURSE_CATALOG_TYPE,
    SINGLE_USE_CODE_REUSE_ERROR,
    SINGLE_USE_REDEEM_URL_REUSE_ERROR,
    SINGLE_USE_VOUCHER_TYPE,
    VALID_DOMAIN_USERS,
    VALID_EMAIL_DOMAINS
)
from regression.pages.ecommerce.redeem_coupon_page import RedeemCouponPage
from regression.pages.whitelabel.const import (
    ORG,
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.helpers.vouchers import VouchersMixin


class TestSingleCourseDiscount(VouchersMixin):
    """
    Tests for Single Course Discount Coupons
    """

    def setUp(self):
        """
        Prepare setup for running tests
        """
        super(TestSingleCourseDiscount, self).setUp()
        # Initialize all page objects
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID[ORG])
        # Initialize common variables
        self.course_id = PROF_COURSE_ID[ORG]
        self.course_price = PROF_COURSE_PRICE[ORG]
        self.course_title = PROF_COURSE_TITLE[ORG]
        self.total_price = PROF_COURSE_PRICE[ORG]

    @skip_cleanup_if_test_passed()
    def test_00_discount_single_use_fixed_code(self):
        """
        Scenario: Discount Single Use Fixed Code: Each code can be used by one
        person successfully
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            SINGLE_USE_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=ABSOLUTE_BENEFIT_TYPE,
            benefit_value=DEFAULT_FIXED_BENEFIT_VALUE,
            quantity=3
        )
        coupon_codes = self.setup_coupons_using_ui(coupon)
        coupon_users = list(COUPON_USERS.values())
        # Login to application using the existing credentials
        self.addCleanup(self.run_full_cleanup)
        for coupon_user, coupon_code in izip(coupon_users, coupon_codes):
            self.login_and_go_to_basket(coupon_user)
            self.enroll_using_discount_code(coupon_code)
            self.assert_enrollment_and_un_enroll()
            self.logout_user_from_lms()

    @skip_cleanup_if_test_passed()
    def test_01_discount_single_use_percentage_code(self):
        """
        Scenario: Discount Single Use Percentage Code: Code cannot be reused
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            SINGLE_USE_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=PERCENTAGE_BENEFIT_TYPE,
            benefit_value=DEFAULT_PERCENTAGE_BENEFIT_VALUE
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        # Login to application using the existing credentials
        self.addCleanup(self.run_full_cleanup)
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_01'])
        self.enroll_using_discount_code(coupon_code)
        self.assert_enrollment_and_un_enroll()
        self.logout_user_from_lms()
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_02'])
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            SINGLE_USE_CODE_REUSE_ERROR.format(coupon_code)
        )

    @skip_cleanup_if_test_passed()
    def test_02_discount_once_per_customer_fixed_code(self):
        """
        Scenario: Discount Once Per Customer Fixed Code: Code can be used up
        to the number of allowed uses and after that it is not usable by anyone
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            ONCE_PER_CUSTOMER_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=ABSOLUTE_BENEFIT_TYPE,
            benefit_value=DEFAULT_FIXED_BENEFIT_VALUE,
            max_uses=2
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        # Login to application using the existing credentials
        coupon_users = list(COUPON_USERS.values())
        last_user = len(coupon_users) - 1
        self.addCleanup(self.run_full_cleanup)
        for i, coupon_user in enumerate(coupon_users):
            self.login_and_go_to_basket(coupon_user)
            if i != last_user:
                self.enroll_using_discount_code(coupon_code)
                self.assert_enrollment_and_un_enroll()
                self.logout_user_from_lms()
            else:
                self.assertEqual(
                    self.error_message_on_invalid_coupon_code(coupon_code),
                    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT
                )

    @skip_cleanup_if_test_passed()
    def test_03_discount_once_per_customer_percentage_code(self):
        """
        Scenario: Discount Once Per Customer Percentage Code: A code cannot
        be used twice by the same user
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            ONCE_PER_CUSTOMER_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=PERCENTAGE_BENEFIT_TYPE,
            benefit_value=DEFAULT_PERCENTAGE_BENEFIT_VALUE
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        self.addCleanup(self.run_full_cleanup)
        # Login to application using the existing credentials
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_01'])
        self.enroll_using_discount_code(coupon_code)
        self.assert_enrollment_and_un_enroll()
        self.dashboard.go_to_find_courses_page()
        # find the target course and click on it to go to about page
        self.find_courses.go_to_course_about_page(self.course_about)
        # go to single seat basket page
        self.course_about.go_to_single_seat_basket_page()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            ONCE_PER_CUSTOMER_CODE_SAME_USER_REUSE.format(coupon_code)
        )

    @skip_cleanup_if_test_passed()
    def test_04_discount_once_per_customer_fixed_code_email_domain(self):
        """
        Scenario: Discount Once Per Customer Fixed Code: Code can be used only
        by users of valid email domains
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            ONCE_PER_CUSTOMER_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=ABSOLUTE_BENEFIT_TYPE,
            benefit_value=DEFAULT_FIXED_BENEFIT_VALUE,
            email_domains=VALID_EMAIL_DOMAINS,
            max_uses=5
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        # Login to application using the existing credentials
        valid_domain_users = list(VALID_DOMAIN_USERS.values())
        invalid_domain_users = list(INVALID_DOMAIN_USERS.values())
        self.addCleanup(self.run_full_cleanup)
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
        self.logout_user_from_ecommerce()
        # Verify that coupon code can be added for authorized email domain
        # In each test we are selecting a random user from the valid domain
        # list to bring down the test run time. Since multiple tests will be
        # running for domain checks, use of random user in all of these will
        # pretty much cover most of the possibilities
        valid_domain_user = random.choice(valid_domain_users)
        self.login_and_go_to_basket(valid_domain_user)
        self.enroll_using_discount_code(coupon_code)
        self.assert_enrollment_and_un_enroll()
        self.logout_user_from_lms()

    def test_05_discount_single_use_fixed_code_expired(self):
        """
        Scenario: Discount Single Use Fixed Code: Relevant error message is
        displayed on the use of Expired coupon
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            SINGLE_USE_VOUCHER_TYPE,
            end_datetime=EXPIRED_END_DATE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=ABSOLUTE_BENEFIT_TYPE,
            benefit_value=DEFAULT_FIXED_BENEFIT_VALUE
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        # Login to application using the existing credentials
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_01'])
        self.assertEqual(
            self.error_message_on_invalid_coupon_code(coupon_code),
            EXPIRED_CODE_ERROR.format(coupon_code)
        )

    @skip_cleanup_if_test_passed()
    def test_06_discount_single_use_fixed_redeem_url(self):
        """
        Scenario: Existing Users - Discount Single Use Fixed Redeem URL: Each
        redeem url can be used by one person successfully
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            SINGLE_USE_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=ABSOLUTE_BENEFIT_TYPE,
            benefit_value=DEFAULT_FIXED_BENEFIT_VALUE,
            quantity=3
        )
        coupon_codes = self.setup_coupons_using_api(coupon)
        # Login to application using the existing credentials
        coupon_users = list(COUPON_USERS.values())
        self.addCleanup(self.run_full_cleanup)
        for coupon_user, coupon_code in izip(coupon_users, coupon_codes):
            self.login_user(coupon_user)
            self.redeem_single_course_discount_coupon(coupon_code, self.basket)
            self.use_discount_redeem_url()
            self.assert_enrollment_and_un_enroll()
            self.logout_user_from_lms()

    def test_07_discount_single_use_percentage_redeem_url(self):
        """
        Scenario: New Activated Users - Discount Single Use Percentage Redeem
        URL: URL cannot be reused
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            SINGLE_USE_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=PERCENTAGE_BENEFIT_TYPE,
            benefit_value=DEFAULT_PERCENTAGE_BENEFIT_VALUE
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        self.addCleanup(self.run_partial_cleanup)
        self.home.visit()
        self.home.go_to_registration_page()
        self.register_user(self.dashboard)
        self.activate_new_user()
        self.redeem_single_course_discount_coupon(coupon_code, self.basket)
        self.use_discount_redeem_url()
        self.assert_enrollment_and_un_enroll()
        self.logout_user_from_lms()
        self.login_user(COUPON_USERS['coupon_user_01'])
        self.redeem_single_course_discount_coupon(
            coupon_code, self.redeem_coupon_error_page)
        self.assertEqual(
            self.redeem_coupon_error_page.error_message,
            SINGLE_USE_REDEEM_URL_REUSE_ERROR
        )

    @skip_cleanup_if_test_passed()
    def test_08_discount_once_per_customer_fixed_redeem_url(self):
        """
        Scenario: Discount Once Per Customer Fixed Redeem URL: Each URL can
        be used up to the number of allowed uses by different users
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            ONCE_PER_CUSTOMER_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=ABSOLUTE_BENEFIT_TYPE,
            benefit_value=DEFAULT_FIXED_BENEFIT_VALUE,
            max_uses=2
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        coupon_users = list(COUPON_USERS.values())
        last_user = len(coupon_users) - 1
        self.addCleanup(self.run_full_cleanup)
        for i, coupon_user in enumerate(coupon_users):
            # Login to course and use coupon
            self.login_user(coupon_user)
            if i != last_user:
                self.redeem_single_course_discount_coupon(
                    coupon_code,
                    self.basket
                )
                self.use_discount_redeem_url()
                self.assert_enrollment_and_un_enroll()
                self.logout_user_from_lms()
            else:
                redeem_coupon = RedeemCouponPage(
                    self.browser, coupon_code).visit()
                self.assertEqual(
                    redeem_coupon.error_message,
                    ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT
                )

    def test_09_discount_once_per_customer_percentage_redeem_url(self):
        """
        Scenario: Inactive Users - Discount Once Per Customer Percentage
        Redeem URL: URL cannot be used twice by he same user
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            ONCE_PER_CUSTOMER_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=PERCENTAGE_BENEFIT_TYPE,
            benefit_value=DEFAULT_PERCENTAGE_BENEFIT_VALUE
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        self.addCleanup(self.run_partial_cleanup)
        self.home.visit()
        self.redeem_single_course_discount_coupon(coupon_code, self.login_page)
        self.login_page.toggle_to_registration_page()
        self.prepare_and_fill_registration_data()
        self.registration.submit_registration_form_data(
            self.redeem_coupon_error_page
        )
        self.assertEqual(
            self.redeem_coupon_error_page.error_message,
            INACTIVE_ACCOUNT_ERROR_MESSAGE
        )
        self.account_activation()
        self.verify_info_is_populated_on_basket()
        self.use_discount_redeem_url()
        self.assert_enrollment_and_un_enroll()
        redeem_coupon = RedeemCouponPage(self.browser, coupon_code).visit()
        self.assertEqual(
            redeem_coupon.error_message,
            ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE
        )

    @skip_cleanup_if_test_passed()
    def test_10_discount_once_per_customer_percentage_redeem_url_email(self):
        """
        Scenario: Discount Once Per Customer Fixed Code: Code can be used only
        by users of valid email domains
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            ONCE_PER_CUSTOMER_VOUCHER_TYPE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=PERCENTAGE_BENEFIT_TYPE,
            benefit_value=DEFAULT_PERCENTAGE_BENEFIT_VALUE,
            email_domains=VALID_EMAIL_DOMAINS,
            max_uses=5
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        valid_domain_users = list(VALID_DOMAIN_USERS.values())
        invalid_domain_users = list(INVALID_DOMAIN_USERS.values())
        self.addCleanup(self.run_full_cleanup)
        # Verify that coupon url cannot be used for unauthorized email domain
        # In each test we are selecting a random user from the invalid domain
        # list to bring down the test run time. Since multiple tests will be
        # running for domain checks, use of random user in all of these will
        # pretty much cover most of the possibilities
        invalid_domain_user = random.choice(invalid_domain_users)
        self.login_user(invalid_domain_user)
        self.redeem_single_course_discount_coupon(
            coupon_code,
            self.redeem_coupon_error_page
        )
        self.assertEqual(
            self.redeem_coupon_error_page.error_message,
            INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL
        )
        self.logout_user_from_ecommerce()
        # Verify that coupon url can be used for authorized email domain
        # In each test we are selecting a random user from the valid domain
        # list to bring down the test run time. Since multiple tests will be
        # running for domain checks, use of random user in all of these will
        # pretty much cover most of the possibilities
        valid_domain_user = random.choice(valid_domain_users)
        self.login_user(valid_domain_user)
        self.redeem_single_course_discount_coupon(coupon_code, self.basket)
        self.use_discount_redeem_url()
        self.assert_enrollment_and_un_enroll()
        self.logout_user_from_lms()

    def test_11_discount_once_per_customer_fixed_redeem_url_future(self):
        """
        Scenario: Discount Once Per Customer Fixed Redeem URL: Relevant error
        message is displayed on the use of future redeem url
        """
        coupon = self.coupon_data(
            SINGLE_COURSE_CATALOG_TYPE,
            DISCOUNT_COUPON_TYPE,
            ONCE_PER_CUSTOMER_VOUCHER_TYPE,
            start_datetime=FUTURE_START_DATE,
            course_id=PROF_COURSE_ID[ORG],
            benefit_type=ABSOLUTE_BENEFIT_TYPE,
            benefit_value=DEFAULT_FIXED_BENEFIT_VALUE,
            max_uses=2
        )
        coupon_code = self.setup_coupons_using_api(coupon)[0]
        self.addCleanup(self.run_partial_cleanup)
        self.login_user(COUPON_USERS['coupon_user_01'])
        redeem_coupon = RedeemCouponPage(self.browser, coupon_code).visit()
        self.assertEqual(redeem_coupon.error_message, FUTURE_REDEEM_URL_ERROR)
