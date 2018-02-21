"""
Tests for enrollment through Otto
"""
from unittest import skipIf

from regression.pages.whitelabel import (
    COURSE_ORG,
    COURSE_NUMBER,
    COURSE_RUN,
    DEFAULT_COURSE_PRICE,
    TEST_ENV
)
from regression.pages.studio.utils import get_course_key
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.helpers.utils import (
    construct_course_basket_page_url,
    get_wl_course_info
)
from regression.tests.whitelabel.course_enrollment_test import (
    CourseEnrollmentTest
)


class TestEnrollmentOtto(CourseEnrollmentTest):
    """
    Tests for Otto Enrollment
    """

    def setUp(self):
        """
        Initialize all objects
        """
        super(TestEnrollmentOtto, self).setUp()
        self.course_info = get_wl_course_info(
            org=COURSE_ORG,
            num=COURSE_NUMBER,
            run=COURSE_RUN
        )
        self.course_id = str(get_course_key(self.course_info))
        self.course_title = self.course_info["display_name"]
        self.course_price = DEFAULT_COURSE_PRICE
        self.total_price = DEFAULT_COURSE_PRICE
        # Initialize page objects
        self.course_about = CourseAboutPage(self.browser, self.course_id)

    @skipIf(TEST_ENV == "stage", "skip tests on stage")
    def test_register_and_select_course(self):
        """
        Scenario: Otto flow - A registered user is able to register, select a
        course and make payment for the course using the credit card
        """
        self.register_using_api()
        self.go_to_basket()
        self.pay_with_cybersource()
        self.dashboard_page.wait_for_page()
        self.assert_course_added_to_dashboard()

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
            construct_course_basket_page_url(self.course_id)
        )
        self.basket_page.wait_for_page()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        self.pay_with_cybersource()
        self.dashboard_page.wait_for_page()
        self.assert_course_added_to_dashboard()
