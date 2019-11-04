"""
Enterprise Offer Discount tests
"""
from __future__ import absolute_import

from regression.pages.common.utils import (
    extract_discount_value_from_response,
    extract_numerical_value_from_price_string
)
from regression.pages.enterprise.enterprise_const import (
    DEFAULT_COURSE_PRICE,
    ENT_CUSTOMER_CATALOG_UUID,
    ENTERPRISE_NAME
)
from regression.pages.whitelabel import ECOM_URL
from regression.pages.whitelabel.basket_page import SingleSeatBasketPage
from regression.tests.enterprise.ent_test_base import EnterpriseTestBase


class TestDiscountEnterpriseOffer(EnterpriseTestBase):
    """
    Tests for Percentage Discount Enterprise Offers
    """
    DISCOUNT_MSG = "Discount provided by "

    def setUp(self):
        super(TestDiscountEnterpriseOffer, self).setUp()
        self.course_price = DEFAULT_COURSE_PRICE
        self.target_url = ECOM_URL + '/enterprise/offers'

    def test_enterprise_percentage_offer(self):
        """
        Scenario: To verify that user sees the correct discount
        percentage info and detail on enterprise landing page,
        basket page and on receipt page.
        """
        # Login user to LMS using staff credentials
        self.login_user_lms_using_api()
        # Get all enterprise offers data using api request
        offers_response = self.login_api.get_offer_request(self.target_url)
        # Get discount value from response against catalog UUID
        discount_value = extract_discount_value_from_response(
            ENT_CUSTOMER_CATALOG_UUID, offers_response
        )
        discounted_course_price = self.course_price - \
            (self.course_price * discount_value) / 100
        self.logout_from_lms_using_api()
        self.ecommerce_courses_page.visit()
        self.register_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        # Get course original price and course discounted price
        price_details = \
            self.ent_course_enrollment.get_course_price_details().split()
        # extract_numerical_value_from_price_string(price_details)
        self.assertEqual(
            self.course_price,
            extract_numerical_value_from_price_string(price_details[1])
        )
        self.assertEqual(
            discounted_course_price,
            extract_numerical_value_from_price_string(price_details[3])
        )
        self.assertIn(
            self.DISCOUNT_MSG + ENTERPRISE_NAME,
            self.ent_course_enrollment.get_course_price_details()
        )
        self.ent_course_enrollment.go_to_data_consent_page()
        self.ent_data_sharing_consent.wait_for_page()
        # Verify that accepting data consent takes user to basket page
        self.ent_data_sharing_consent.accept_data_sharing_consent()

        SingleSeatBasketPage(self.browser).wait_for_page()
        self.verify_info_is_populated_on_basket(
            discounted_course_price
        )
        self.verify_receipt_info_for_discounted_course()
