"""
Tests for existing users using Otto
"""
import uuid
from unittest import skip

from regression.pages.common.email_client import GuerrillaMailApi
from regression.pages.ecommerce.basket_page import SingleSeatBasketPage
from regression.pages.whitelabel.const import (
    EXISTING_USER_EMAIL,
    PASSWORD,
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.course_info_page import CourseInfoPage
from regression.pages.whitelabel.home_page import HomePage
from regression.tests.helpers.course_enrollment import CourseEnrollmentMixin


class TestExistingUserOtto(CourseEnrollmentMixin):
    """
    Tests for Otto Enrollment for Existing Users
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestExistingUserOtto, self).setUp()
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID)
        self.course_info = CourseInfoPage(self.browser, PROF_COURSE_ID)
        self.home = HomePage(self.browser)
        self.single_seat_basket = SingleSeatBasketPage(self.browser)
        # Initialize common objects
        self.course_id = PROF_COURSE_ID
        self.course_title = PROF_COURSE_TITLE
        self.course_price = PROF_COURSE_PRICE
        self.total_price = PROF_COURSE_PRICE

    @skip('remove after WL-1058 is fixed')
    def test_00_login_and_select_course(self):
        """
        Scenario: Otto flow - A registered user is able to login, select a
        course and make payment for the course using the credit card
        """
        self.addCleanup(
            self.unenroll_using_api,
            EXISTING_USER_EMAIL,
            self.course_id
        )
        self.login_and_go_to_basket(EXISTING_USER_EMAIL)
        self.pay_with_cybersource()
        self.assert_enrollment_and_logout()

    @skip('disabling temporarily due to an issue with chrome on jenkins')
    def test_01_select_course_and_login(self):
        """
        Scenario: Otto flow - A registered user is able to select a course,
        login  and make payment for the course using the credit card
        """
        self.addCleanup(
            self.unenroll_using_api,
            EXISTING_USER_EMAIL,
            self.course_id
        )
        self.home.visit()
        self.home.go_to_courses_page()
        self.find_courses.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        self.course_about.register_using_enrollment_button()
        self.registration.toggle_to_login_page()
        self.login_page.authenticate_user(
            EXISTING_USER_EMAIL,
            PASSWORD,
            self.basket
        )
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        self.pay_with_cybersource()
        self.assert_enrollment_and_logout()

    @skip('This test requires access to gmail, currently we are using an alternate test')
    def test_07_multi_seat_flow(self):
        """
        Scenario: Otto Group Purchase - An existing user is able to register
        for a course and make payment for multiple seats in the course using
        the credit card
        """
        self.temp_mail = GuerrillaMailApi()
        user_name = str(uuid.uuid4().node)
        self.user_email = self.temp_mail.get_email_account(user_name)
        seat_counter = 3
        # Login to application using the existing credentials
        self.login_user(self.user_email)
        # click on the target course to go to it's about page
        self.dashboard.go_to_find_courses_page()
        # find the target course and click on it to go to about page
        self.find_courses.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        # Check that group purchase button is now present
        self.assertTrue(self.course_about.is_group_purchase_button_present())
        # go to multi seat basket page
        self.course_about.go_to_multi_seat_basket_page()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        # increase number of seats
        self.increase_seats(seat_counter)
        # course price and total price after increasing seats
        self.course_price = PROF_COURSE_PRICE * seat_counter
        self.total_price = PROF_COURSE_PRICE * seat_counter
        self.verify_price_on_basket()
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Application should take user to the receipt page
        # Verify on receipt page that information like course title, course
        # price, total price order date and billing to is displayed correctly
        self.verify_receipt_info()
        self.receipt.go_to_dashboard()
        self.assertFalse(self.dashboard.is_course_present(self.course_id))
        self.logout_user_from_lms()
        enrollment_file_link = self.get_url_from_email(
            self.user_email,
            'enrollment_code_csv'
        )
        coupons = self.get_bulk_purchase_enrollment_codes(
            self.user_email,
            PASSWORD,
            enrollment_file_link
        )
        self.assertEqual(len(coupons), seat_counter)
