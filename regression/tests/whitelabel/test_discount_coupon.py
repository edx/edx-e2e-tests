"""
Single course Discount coupons tests
"""
import random
import uuid
from itertools import izip

from regression.tests.helpers.coupon_consts import (
    BENEFIT_TYPE,
    BENEFIT_VALUE,
    COUPON_USERS,
    COUPON_TYPE,
    COURSE_CATALOG_TYPE,
    EXPIRED_CODE_ERROR,
    EXPIRED_END_DATE,
    FUTURE_START_DATE,
    FUTURE_REDEEM_URL_ERROR,
    INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET,
    INVALID_DOMAIN_USERS,
    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT,
    ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE,
    SEAT_TYPE,
    SINGLE_USE_CODE_REUSE_ERROR,
    STOCK_RECORD_ID,
    VALID_DOMAIN_USERS,
    VALID_EMAIL_DOMAINS,
    VOUCHER_TYPE
)

from regression.pages.whitelabel.const import (
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE,
    PASSWORD
)

from regression.tests.whitelabel.voucher_tests_base import VouchersTest
from regression.pages.whitelabel.inactive_account import InactiveAccount
from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.utils import activate_account
from regression.pages.whitelabel.redeem_coupon_page import (
    RedeemCouponPage
)
from regression.tests.helpers.utils import get_white_label_registration_fields
from regression.tests.helpers.api_clients import GuerrillaMailApi


class TestDiscountCoupon(VouchersTest):
    """
    Tests for Single Course Discount Coupons
    """
    def setUp(self):
        super(TestDiscountCoupon, self).setUp()
        # Initialize all page objects
        # Initialize common variables
        self.course_id = PROF_COURSE_ID
        self.course_price = PROF_COURSE_PRICE
        self.course_title = PROF_COURSE_TITLE
        self.total_price = PROF_COURSE_PRICE

    def test_discount_single_use_percentage_code(self):
        """
        Scenario: Discount Single Use Percentage Code: Code cannot be reused
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['single'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            benefit_type=BENEFIT_TYPE['per'],
            benefit_value=BENEFIT_VALUE['per']
        )
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        self.addCleanup(self.coupon.delete_coupon)
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

    def test_discount_once_per_customer_fixed_code(self):
        """
        Scenario: Discount Once Per Customer Fixed Code: Code can be used up
        to the number of allowed uses and after that it is not usable by anyone
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
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
                self.enroll_using_discount_code(coupon_code)
                self.assert_enrollment_and_logout()
            else:
                self.assertEqual(
                    self.error_message_on_invalid_coupon_code(coupon_code),
                    ONCE_PER_CUSTOMER_CODE_MAX_LIMIT
                )

    def test_discount_once_per_customer_fixed_code_email_domain(self):
        """
        Scenario: Discount Once Per Customer Fixed Code: Code can be used only
        by users of valid email domains
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
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
        self.enroll_using_discount_code(coupon_code)
        self.assert_enrollment_and_logout()

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
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed']
        )

        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        # Login to application using the existing credentials
        self.login_and_go_to_basket(COUPON_USERS['coupon_user_01'])
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
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
            quantity=3
        )

        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_codes = self.coupon.coupon_codes
        # Login to application using the existing credentials
        coupon_users = list(COUPON_USERS.values())
        for coupon_user, coupon_code in izip(coupon_users, coupon_codes):
            self.addCleanup(
                self.unenroll_using_api,
                coupon_user,
                self.course_id
            )
            self.login_page.visit()
            self.login_user_using_ui(coupon_user, PASSWORD)
            self.redeem_single_course_discount_coupon(coupon_code)
            self.basket_page.wait_for_page()
            self.use_discount_redeem_url()
            self.dashboard_page.wait_for_page()
            self.assert_enrollment_and_logout()

    def test_discount_once_per_customer_percentage_redeem_url(self):
        """
        Scenario: Inactive Users - Discount Once Per Customer Percentage
        Redeem URL: URL cannot be used twice by he same user
        """
        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['once_per_cust'],
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            benefit_type=BENEFIT_TYPE['per'],
            benefit_value=BENEFIT_VALUE['per']
        )

        inactive_account = InactiveAccount(self.browser)
        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]
        self.home.visit()
        self.redeem_single_course_discount_coupon(coupon_code)
        self.login_page.wait_for_page()
        self.login_page.toggle_to_registration_page()
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

        inactive_account.wait_for_page()
        self.assertTrue(inactive_account.is_activation_message_present())
        activate_account(self, temp_mail)
        self.verify_info_is_populated_on_basket(
            self.coupon.discounted_course_price
        )
        self.use_discount_redeem_url()
        self.assert_enrollment_and_unenroll()
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
            course_id=PROF_COURSE_ID,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=STOCK_RECORD_ID,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
            max_uses=2
        )

        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_code = self.coupon.coupon_codes[0]

        self.login_page.visit()
        self.login_user_using_ui(COUPON_USERS['coupon_user_01'], PASSWORD)

        # self.login_user(COUPON_USERS['coupon_user_01'])
        self.addCleanup(
            self.unenroll_using_api,
            COUPON_USERS['coupon_user_01'],
            self.course_id
        )
        redeem_coupon = RedeemCouponPage(self.browser, coupon_code).visit()
        self.assertEqual(
            redeem_coupon.error_message,
            FUTURE_REDEEM_URL_ERROR
        )
