"""
End to end tests for User Donations.
"""
from unittest import skip
from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.register_page import RegisterPageExtended
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.course_drupal_page import (
    DemoCourseSelectionPage
)
from regression.pages.lms.payment_confirmation_page import (
    PaymentConfirmationPage
)
from regression.pages.lms.checkout_page import PaymentPage


class DonationsTest(WebAppTest):
    """
    Regression tests of Donations
    """

    def setUp(self):
        super(DonationsTest, self).setUp()
        self.register_page = RegisterPageExtended(self.browser)
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.drupal_course_page = DemoCourseSelectionPage(self.browser)
        self.payment_page = PaymentPage(self.browser)
        self.payment_confirmation_page = PaymentConfirmationPage(self.browser)

        # Navigate to the registration page
        self.register_page.visit()

        # Create random email and register
        username = "test_{uuid}".format(uuid=self.unique_id[0:6])
        email = "{user}@example.com".format(user=username)
        self.register_page.register(
            email=email,
            password="edx",
            username=username,
            full_name="Test User",
            country="US",
            favorite_movie="Some Movie",
            terms_of_service=True
        )
        self.dashboard_page.wait_for_page()

    @skip('This test needs to be updated. See LT-48')
    def test_user_donations(self):
        """
        Verifies that user can Donate after selecting a course for audit
        """
        self.drupal_course_page.visit()
        self.drupal_course_page.click_enroll_now()
        self.dashboard_page.wait_for_page()
        self.dashboard_page.click_donate_button()
        self.payment_page.wait_for_page()
        self.payment_page.make_test_payment()
        self.payment_confirmation_page.wait_for_page()
