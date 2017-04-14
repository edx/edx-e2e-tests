"""
Tests for new users using Otto
"""
from unittest import skip
from regression.pages.whitelabel.const import (
    PASSWORD,
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.course_info_page import CourseInfoPage
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.inactive_account import InactiveAccount
from regression.tests.helpers.course_enrollment import CourseEnrollmentMixin


class TestNewUserOtto(CourseEnrollmentMixin):
    """
    Tests for Otto Enrollment for New Users
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestNewUserOtto, self).setUp()
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID)
        self.course_info = CourseInfoPage(self.browser, PROF_COURSE_ID)
        self.home = HomePage(self.browser)
        self.inactive_account = InactiveAccount(self.browser)
        # Initialize common objects
        self.course_id = PROF_COURSE_ID
        self.course_title = PROF_COURSE_TITLE
        self.course_price = PROF_COURSE_PRICE
        self.total_price = PROF_COURSE_PRICE

    def test_01_select_course_and_register(self):
        """
        Scenario: Otto Flow - A new user is able to select a course, register
        and make payment for the course using the credit card
        """
        # Open the home page as a new unregistered used
        self.find_courses.visit()
        # click on the target course to go to it's about page
        self.find_courses.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        # register for course
        self.course_about.register_using_enrollment_button()
        self.register_user(self.inactive_account)
        # Application should take user to the page where activate account
        # message is displayed
        self.assertTrue(self.inactive_account.is_activation_message_present())
        self.account_activation()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Application should take user to the receipt page
        # Verify on receipt page that information like course title, course
        # price, total price order date and billing to is displayed correctly
        self.verify_receipt_info()
        self.receipt.go_to_dashboard()
        # Verify that course is added to user dashboard and user can access
        # the course
        self.assertTrue(self.is_course_added_to_dashboard())

    def test_02_register_and_select_course(self):
        """
        Scenario: Otto flow - A new user is able to register, select a course
        and make payment for the course using the credit card
        """
        # Go to registration page and register for the course
        self.home.visit()
        self.home.go_to_registration_page()
        self.register_user(self.dashboard)
        # click on the target course to go to it's about page
        self.dashboard.go_to_find_courses_page()
        # find the target course and click on it to go to about page
        self.find_courses.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        # Verify that clicking on Enroll button takes inactive user to
        # activation page
        self.course_about.go_to_inactive_page()
        # activate the account which should lead user to basket page
        self.account_activation()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Application should take user to the receipt page
        # Verify on receipt page that information like course title,
        # course price, total price
        # order date and billing to is displayed correctly
        self.verify_receipt_info()
        self.receipt.go_to_dashboard()
        # Verify that course is added to user dashboard and user can access
        # the course
        self.assertTrue(self.is_course_added_to_dashboard())

    @skip('disabling temporarily due to an issue with email handling')
    def test_03_multi_seat_flow(self):
        """
        Scenario: Otto Group Purchase - A new user is able to register,
        select a course and make payment for the course using the credit card
        """
        seat_counter = 3
        # Login to application using the existing credentials
        # Go to registration page and register for the course
        self.home.visit()
        self.home.go_to_registration_page()
        self.register_user(self.dashboard)
        # click on the target course to go to it's about page
        self.dashboard.go_to_find_courses_page()
        # find the target course and click on it to go to about page
        self.find_courses.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        # Check that group purchase button is not present
        self.assertFalse(self.course_about.is_group_purchase_button_present())
        self.account_activation()
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
        # Go to next page to make the payment
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
            'enrollment codes',
            'enrollment_code_csv'
        )
        coupons = self.get_bulk_purchase_enrollment_codes(
            self.user_email,
            PASSWORD,
            enrollment_file_link
        )
        self.assertEqual(len(coupons), seat_counter)
