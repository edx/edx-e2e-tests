"""
Single course Discount coupons tests
"""
from __future__ import absolute_import

import logging
import random
import uuid
from unittest import skip, skipIf
from bok_choy.browser import save_screenshot

from regression.pages.studio.utils import get_course_key
from regression.pages.whitelabel import (
    COURSE_NUMBER, COURSE_ORG, COURSE_RUN,
    DEFAULT_COURSE_PRICE, TEST_ENV
)
from regression.pages.whitelabel.const import PASSWORD
from regression.pages.whitelabel.redeem_coupon_page import RedeemCouponPage
from regression.tests.helpers.coupon import Coupon
from regression.tests.helpers.coupon_consts import (
    BENEFIT_TYPE, BENEFIT_VALUE, COUPON_TYPE, COURSE_CATALOG_TYPE,
    EXPIRED_CODE_ERROR, EXPIRED_END_DATE, FUTURE_REDEEM_URL_ERROR,
    FUTURE_START_DATE, INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET,
    INVALID_DOMAIN_USERS, ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE,
    SEAT_TYPE, SINGLE_USE_CODE_REUSE_ERROR, VALID_EMAIL_DOMAIN, VOUCHER_TYPE
)
from regression.tests.helpers.utils import (
    construct_course_basket_page_url,
    get_white_label_registration_fields,
    get_wl_course_info
)
from regression.tests.whitelabel.voucher_tests_base import VouchersTest
import requests


log = logging.getLogger(__name__)


class TestDiscountCoupon(VouchersTest):
    """
    Tests for Single Course Discount Coupons
    """
    def setUp(self):
        super(TestDiscountCoupon, self).setUp()
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

    def test_discount_single_use_fixed_redeem_url(self):
        """
        Scenario: Existing Users - Discount Single Use Fixed Redeem URL: Each
        redeem url can be used by one person successfully
        """
        log.error("Can you see this???")

        self.coupon = Coupon(
            COURSE_CATALOG_TYPE['single'],
            COUPON_TYPE['disc'],
            VOUCHER_TYPE['single'],
            course_id=self.course_id,
            seat_type=SEAT_TYPE['prof'],
            stock_record_ids=self.stock_record_id,
            benefit_type=BENEFIT_TYPE['abs'],
            benefit_value=BENEFIT_VALUE['fixed'],
            quantity=2
        )

        self.coupon.setup_coupons_using_api(self.course_price)
        coupon_codes = self.coupon.coupon_codes
        log.error("Created coupon code: %s", str(coupon_codes))

        # Delete coupon after test
        # self.addCleanup(self.coupon.delete_coupon)

        for coupon_code in coupon_codes:
            log.error("Starting test with coupon code: %s", coupon_code)

            # Register to application using api
            save_screenshot(self.driver, 'zz_' + coupon_code + '_1_before_register_using_api')
            self.register_using_api()
            save_screenshot(self.driver, 'zz_' + coupon_code + '_2_after_register_using_api')
            log.error("Completed register_using_api()")
            self.redeem_single_course_discount_coupon(coupon_code)

            log.error("Completed redeem_single_course_discount_coupon()")
            self.basket_page.wait_for_page()
            save_screenshot(self.driver, 'zz_' + coupon_code + '_4_after_redeem_single_course_discount_coupon')
            log.error("Completed basket_page.wait_for_page()")
            self.ecom_cookies = self.browser.get_cookies()
            log.error("Saved cookies: %s", str(self.ecom_cookies))
            self.make_payment_after_discount(coupon_code)
            log.error("Completed make_payment_after_discount()")
            self.dashboard_page.wait_for_page()
            log.error("Completed dashboard_page.wait_for_page()")
            self.assert_enrollment_and_logout()

            save_screenshot(self.driver, 'zz_' + coupon_code + '_6_after_logout')
            log.error("Completed assert_enrollment_and_logout()")
            log.error("Cookies after logout: %s", str(self.browser.get_cookies()))
