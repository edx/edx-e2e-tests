"""
Tests for enrollment through Otto
"""
from regression.pages.whitelabel.const import (
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.helpers.utils import construct_course_basket_page_url
from regression.tests.whitelabel.course_enrollment_test import (
    CourseEnrollmentTest
)


class TestEnrollmentOtto(CourseEnrollmentTest):
    """
    Tests for Otto Enrollment
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestEnrollmentOtto, self).setUp()
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID)
        # Initialize common objects
        self.course_id = PROF_COURSE_ID
        self.course_title = PROF_COURSE_TITLE
        self.course_price = PROF_COURSE_PRICE
        self.total_price = PROF_COURSE_PRICE

    def test_register_and_select_course(self):
        """
        Scenario: Otto flow - A registered user is able to register, select a
        course and make payment for the course using the credit card
        """
        self.register_using_api()
        self.go_to_basket()
        self.pay_with_cybersource()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout()

    def test_select_course_and_register(self):
        """
        Scenario: Otto flow - A user is able to select a course,
        register  and make payment for the course using the credit card
        """
        self.home_page.visit()
        self.home_page.go_to_courses_page()
        self.courses_page.wait_for_page()
        self.courses_page.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        self.course_about.register_using_enrollment_button()
        self.registration_page.wait_for_page()
        # Register a user using api and send it course specific basket page
        # as target page
        self.register_using_api(
            construct_course_basket_page_url(PROF_COURSE_ID)
        )
        self.basket_page.wait_for_page()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        self.pay_with_cybersource()
        self.dashboard_page.wait_for_page()
        self.assert_enrollment_and_logout()
