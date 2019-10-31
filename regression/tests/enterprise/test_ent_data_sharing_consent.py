"""
Enterprise Data consent tests
"""
from __future__ import absolute_import

from regression.pages.enterprise.enterprise_const import ENT_COURSE_TITLE, ENTERPRISE_NAME
from regression.pages.whitelabel.basket_page import SingleSeatBasketPage
from regression.tests.enterprise.ent_test_base import EnterpriseTestBase


class TestEnterpriseDataSharingConsent(EnterpriseTestBase):
    """
    Test Enterprise Data Consent
    """

    CONSENT_MSG = "To access this course, you must first consent to share"
    CONSENT_DECLINE_WARNING = "We could not enroll you"

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestEnterpriseDataSharingConsent, self).setUp()
        self.browser.maximize_window()

    def test_data_sharing_consent_page_details(self):
        """
        Scenario: To verify that user sees the correct settings on data consent
            page
            Given that a new user registers for the course through enterprise
            When this user clicks next from enrollment page
            Then this user is taken to data consent page
            And relevant details are shown on this page
        """
        self.register_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        self.assertEqual(
            ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        self.ent_course_enrollment.go_to_data_consent_page()
        self.ent_data_sharing_consent.wait_for_page()
        # Verify consent text
        self.assertIn(
            self.CONSENT_MSG,
            self.ent_data_sharing_consent.get_consent_message_text()
        )
        # Verify enterprise name in consent text
        self.assertEqual(
            ENTERPRISE_NAME,
            self.ent_data_sharing_consent.get_enterprise_name_from_msg()
        )
        # Verify that user is able to open policy dropdown from policy link
        self.ent_data_sharing_consent.open_policy_text()

    def test_data_sharing_consent_acceptance(self):
        """
        Scenario: To verify that user is taken to basket page on accepting
            data consent
            Given that a user is on data consent page
            When this user checks the data consent check box
            And Clicks on the Continue button
            Then this user is taken to basket page
        """
        self.ecommerce_courses_page.visit()
        self.register_and_go_to_course_enrollment_page()
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

    def test_data_sharing_consent_rejection(self):
        """
        Scenario: To verify that user is taken back to enrollment page on
            declining data consent
            Given that a user is on data consent page
            When this user decline the data consent
            Then this user is taken shown a message
            And this user is taken back to Enrollment page
            And this user is shown a warning on Enrollment page
        """
        self.register_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        self.assertEqual(
            ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        self.ent_course_enrollment.go_to_data_consent_page()
        self.ent_data_sharing_consent.wait_for_page()
        # Verify that declining data consent takes user back to enrollment
        # page where a warning is shown
        self.ent_data_sharing_consent.decline_data_sharing_consent()
        self.assertIn(
            self.CONSENT_DECLINE_WARNING,
            self.ent_course_enrollment.get_data_sharing_consent_warning()
        )
