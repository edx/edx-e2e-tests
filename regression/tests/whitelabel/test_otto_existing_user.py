"""
Tests for existing users using Otto
"""
from unittest import skip

from regression.pages.whitelabel.const import (
    EXISTING_USER_EMAIL,
    PASSWORD,
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.whitelabel.course_enrollment_test import (
    CourseEnrollmentTest
)


class TestExistingUserOtto(CourseEnrollmentTest):
    """
    Tests for Otto Enrollment for Existing Users
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestExistingUserOtto, self).setUp()
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID)
        # Initialize common objects
        self.course_id = PROF_COURSE_ID
        self.course_title = PROF_COURSE_TITLE
        self.course_price = PROF_COURSE_PRICE
        self.total_price = PROF_COURSE_PRICE

        self.addCleanup(
            self.unenroll_using_api,
            EXISTING_USER_EMAIL,
            self.course_id
        )

    @skip
    def test_login_and_select_course(self):
        """
        Scenario: Otto flow - A registered user is able to login, select a
        course and make payment for the course using the credit card
        """
        self.login_and_go_to_basket(EXISTING_USER_EMAIL)
        self.pay_with_cybersource()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout()

    @skip
    def test_select_course_and_login(self):
        """
        Scenario: Otto flow - A registered user is able to select a course,
        login  and make payment for the course using the credit card
        """
        self.home_page.visit()
        self.home_page.go_to_courses_page()
        self.courses_page.wait_for_page()
        self.courses_page.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        self.course_about.register_using_enrollment_button()
        self.registration_page.wait_for_page()
        self.registration_page.toggle_to_login_page()
        self.login_page.wait_for_page()
        self.login_page.authenticate_user(
            EXISTING_USER_EMAIL,
            PASSWORD
        )
        self.basket_page.wait_for_page()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        self.pay_with_cybersource()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout()
