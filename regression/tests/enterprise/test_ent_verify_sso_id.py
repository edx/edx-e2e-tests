"""
Enterprise SSO ID Verification tests
"""
from __future__ import absolute_import

from regression.pages.enterprise.enterprise_const import ENT_COURSE_ID, ENT_COURSE_TITLE
from regression.pages.whitelabel.basket_page import SingleSeatBasketPage
from regression.tests.enterprise.ent_test_base import EnterpriseTestBase


class TestEnterpriseSSOIDVerification(EnterpriseTestBase):
    """
    Test Enterprise ID Verification page
    """

    def test_enterprise_user_id_verification_status(self):
        """
        Scenario: To verify that enterprise user ID automatically verified
         during SSO process
            Given that a user is on data consent page
            When this user checks the data consent check box
            And Clicks on the Continue button
            Then this user is taken to basket page
            complete payment process
            Then user should not see any ID verification panel
            on receipt page as enterprise learners ID
            automatically verified if enterprise SSO settings enabled
            in admin configuration.
        """
        self.ecommerce_courses_page.visit()
        self.register_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        self.assertEqual(
            ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        self.ent_course_enrollment.go_to_data_consent_page()
        self.ent_data_sharing_consent.wait_for_page()
        # Verify that accepting data consent takes user to basket page
        self.ent_data_sharing_consent.accept_data_sharing_consent()
        SingleSeatBasketPage(self.browser).wait_for_page()
        self.payment_using_cyber_source()
        self.assertIn(ENT_COURSE_TITLE, self.receipt_page.order_desc)
        # Enterprise user ID is already verified as learner go through
        # the SSO process, so no ID verification panel appears on receipt page
        self.assertFalse(self.receipt_page.get_id_verification_panel_status())
        self.receipt_page.click_in_nav_to_go_to_dashboard()

    def test_edx_user_id_verification_status(self):
        """
        Scenario: To verify that non enterprise learner ID
        is not verified and ID verification panel visible on
        receipt page.
        """
        self.ecommerce_courses_page.visit()
        self.register_edx_user()
        self.dashboard.click_explore_courses_link()
        # self.courses_page.wait_for_page()
        self.courses_page.click_on_the_course(ENT_COURSE_ID)
        self.course_about_page.wait_for_page()
        self.assertEqual(
            ENT_COURSE_TITLE,
            self.course_about_page.get_course_title()
        )
        self.course_about_page.click_enroll_button()
        self.track_selection_page.wait_for_page()
        self.track_selection_page.click_verified_mode()
        SingleSeatBasketPage(self.browser).wait_for_page()
        self.payment_using_cyber_source()
        self.assertIn(ENT_COURSE_TITLE, self.receipt_page.order_desc)
        # User ID is not verified,
        # so ID verification panel appears on receipt page
        self.assertTrue(self.receipt_page.get_id_verification_panel_status())
