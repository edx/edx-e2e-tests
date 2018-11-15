"""
Enterprise Offer Discount tests
"""
from regression.tests.enterprise.ent_test_base import EnterpriseTestBase
from regression.pages.whitelabel.basket_page import SingleSeatBasketPage


class TestDiscountEnterpriseOffer(EnterpriseTestBase):
    """
    Tests for Percentage Discount Enterprise Offers
    """
    DISCOUNT_MSG = "Discount provided by "

    def setUp(self):
        super(TestDiscountEnterpriseOffer, self).setUp()

    def test_percentage_offer_detail_landing_page(self):
        """
        Scenario: To verify that user sees the correct discount
        percentage info and detail on enterprise landing page
        Given a user has an edx account which is linked to an Enterprise
        portal account When this user lands on the enrollment landing page
        Then this user is shown correct discount details
        """
        self.register_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        self.assertEqual(
            self.ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        # Verify that course type "verified" is present as a selectable option
        self.assertTrue(
            self.ent_course_enrollment.target_course_type_is_present(
                "verified"
            )
        )
        self.assertIn(
            self.ENT_COURSE_PRICE,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.assertIn(
            self.ENT_COURSE_DISCOUNTED_PRICE,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.assertIn(
            self.DISCOUNT_MSG + self.ENT_NAME,
            self.ent_course_enrollment.get_course_discounted_price()
        )

    def test_percentage_offer_detail_basket_page(self):
        """
        Scenario: To verify that user sees the correct discount
        percentage info and detail on basket page
        """
        self.ecommerce_courses_page.visit()
        self.register_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        self.assertEqual(
            self.ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        # Verify that course type "verified" is present as a selectable option
        self.assertTrue(
            self.ent_course_enrollment.target_course_type_is_present(
                "verified"
            )
        )
        self.assertIn(
            self.ENT_COURSE_PRICE,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.assertIn(
            self.ENT_COURSE_DISCOUNTED_PRICE,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.assertIn(
            self.DISCOUNT_MSG + self.ENT_NAME,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.ent_course_enrollment.go_to_data_consent_page()
        self.ent_data_sharing_consent.wait_for_page()
        # Verify that accepting data consent takes user to basket page
        self.ent_data_sharing_consent.accept_data_sharing_consent()
        SingleSeatBasketPage(self.browser).wait_for_page()
        self.verify_info_is_populated_on_basket(
            self.ENT_COURSE_DISCOUNTED_PRICE
        )

    def test_enterprise_percentage_offer(self):
        """
        Scenario: To verify that user sees the correct discount
        percentage info and detail on enterprise landing page,
        basket page and on receipt page.
        """
        self.ecommerce_courses_page.visit()
        self.register_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        self.assertEqual(
            self.ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        # Verify that course type "verified" is present as a selectable option
        self.assertTrue(
            self.ent_course_enrollment.target_course_type_is_present(
                "verified"
            )
        )
        self.assertIn(
            self.ENT_COURSE_PRICE,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.assertIn(
            self.ENT_COURSE_DISCOUNTED_PRICE,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.assertIn(
            self.DISCOUNT_MSG + self.ENT_NAME,
            self.ent_course_enrollment.get_course_discounted_price()
        )
        self.ent_course_enrollment.go_to_data_consent_page()
        self.ent_data_sharing_consent.wait_for_page()
        # Verify that accepting data consent takes user to basket page
        self.ent_data_sharing_consent.accept_data_sharing_consent()

        SingleSeatBasketPage(self.browser).wait_for_page()
        self.verify_info_is_populated_on_basket(
            self.ENT_COURSE_DISCOUNTED_PRICE
        )
        self.payment_using_cyber_source()
        self.verify_receipt_info_for_discounted_course()
