"""
Tests for existing users using Otto
"""
import unittest

from regression.pages.ecommerce.back_to_basket_page import BackToBasketPage
from regression.pages.ecommerce.basket_page import SingleSeatBasketPage
from regression.pages.ecommerce.cancel_checkout_page import CancelCheckoutPage
from regression.pages.whitelabel.const import (
    TEST_EMAIL_ACCOUNT,
    EXISTING_USER_EMAIL,
    ORG,
    PASSWORD,
    PROF_COURSE_ID,
    PROF_COURSE_TITLE,
    PROF_COURSE_PRICE,
    URL_WITHOUT_AUTH
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
        self.back_to_basket_page = BackToBasketPage(self.browser)
        self.cancel_checkout_page = CancelCheckoutPage(self.browser)
        self.course_about = CourseAboutPage(self.browser, PROF_COURSE_ID)
        self.course_info = CourseInfoPage(self.browser, PROF_COURSE_ID)
        self.home = HomePage(self.browser)
        self.single_seat_basket = SingleSeatBasketPage(self.browser)
        # Initialize common objects
        self.course_id = PROF_COURSE_ID
        self.course_title = PROF_COURSE_TITLE
        self.course_price = PROF_COURSE_PRICE
        self.total_price = PROF_COURSE_PRICE

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

    def test_02_switch_between_single_seat_and_multi_seat_baskets(self):
        """
        Scenario: Otto flow - A user is able to switch from single seat basket
        page to multi seat basket page and vice versa
        """
        # Login to application using the existing credentials
        self.login_and_go_to_basket(EXISTING_USER_EMAIL)
        # Verify that voucher link is present on single seat basket
        self.single_seat_basket.is_voucher_link_visible()
        # Verify that multi seat link is present
        self.assertTrue(
            self.single_seat_basket.is_multi_seat_basket_link_visible())
        # Go to Multi seat Basket page
        self.single_seat_basket.go_to_multi_seat_basket()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        # Verify that multi seat selector is present on the page
        self.multi_seat_basket.is_multi_seat_selector_visible()
        # Verify that single seat link is present
        self.assertTrue(
            self.multi_seat_basket.is_single_seat_basket_link_visible()
        )
        # Switch back to Single seat basket
        self.multi_seat_basket.go_to_single_seat_basket()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()
        # Verify that voucher link is present on single seat basket
        self.single_seat_basket.is_voucher_link_visible()
        # Verify that multi seat link is present
        self.assertTrue(
            self.single_seat_basket.is_multi_seat_basket_link_visible()
        )

    @unittest.skipUnless(ORG == 'MITProfessionalX', 'Run only for MITProfEd')
    def test_03_single_seat_purchase_use_back_button_on_checkout_page(self):
        """
        Scenario: Otto flow - Single Seat - User is taken to a page with
        relevant error message when back button is used on checkout page
        """
        self.login_and_go_to_basket(EXISTING_USER_EMAIL)
        self.basket.go_to_cybersource_page()
        self.cyber_source.go_back_to_basket_page()
        # Verify error message header
        self.assertEqual(
            self.back_to_basket_page.error_message_header,
            'Your purchase could not be completed'
        )
        # Verify that dashboard link and correct support email address
        # is present in error message
        self.assertIn(
            URL_WITHOUT_AUTH,
            self.back_to_basket_page.dashboard_link_in_error_message
        )
        # Condition commented due to existing bug WL-578
        # self.assertIn(
        # EMAIL_SENDER_ACCOUNT,
        # self.back_to_basket_page.support_email_in_error_message
        # )

    def test_04_single_seat_purchase_cancel_checkout(self):
        """
        Scenario: Otto flow - Single Seat - User is taken to a page with
        relevant error message when payment is cancelled from checkout page
        """
        self.login_and_go_to_basket(EXISTING_USER_EMAIL)
        self.basket.go_to_cybersource_page()
        self.cyber_source.cancel_checkout()
        # Verify error message header
        self.assertEqual(
            self.cancel_checkout_page.error_message_header,
            'Checkout Cancelled'
        )
        # Verify that correct support email address is present in error message
        # Condition commented due to existing bug WL-579
        # self.assertIn(
        # EMAIL_SENDER_ACCOUNT,
        # self.cancel_checkout.support_email_in_error_message
        # )

    @unittest.skipUnless(ORG == 'MITProfessionalX', 'Run only for MITProfEd')
    def test_05_bulk_purchase_use_back_button_on_checkout_page(self):
        """
        Scenario: Otto flow - Bulk Purchase - User is taken to a page with
        relevant error message when back button is used on checkout page
        """
        self.login_and_go_to_basket(EXISTING_USER_EMAIL, bulk_purchase=True)
        self.basket.go_to_cybersource_page()
        self.cyber_source.go_back_to_basket_page()
        # Verify error message header
        self.assertEqual(
            self.back_to_basket_page.error_message_header,
            'Your purchase could not be completed'
        )
        # Verify that dashboard link and correct support email address is
        # present in error message
        self.assertIn(
            URL_WITHOUT_AUTH,
            self.back_to_basket_page.dashboard_link_in_error_message
        )
        # Condition commented due to existing bug WL-579
        # self.assertIn(
        # EMAIL_SENDER_ACCOUNT,
        # self.back_to_basket_page.support_email_in_error_message
        # )

    def test_06_bulk_purchase__cancel_checkout(self):
        """
        Scenario: Otto flow - Bulk Purchase - User is taken to a page with
        relevant error message when payment is cancelled from checkout page
        """
        self.login_and_go_to_basket(EXISTING_USER_EMAIL, bulk_purchase=True)
        self.basket.go_to_cybersource_page()
        self.cyber_source.cancel_checkout()
        # Verify error message header
        self.assertEqual(
            self.cancel_checkout_page.error_message_header,
            'Checkout Cancelled'
        )
        # Verify that correct support email address is present in error message
        # Condition commented due to existing bug WL-579
        # self.assertIn(
        # EMAIL_SENDER_ACCOUNT,
        # self.cancel_checkout.support_email_in_error_message
        # )

    def test_07_multi_seat_flow(self):
        """
        Scenario: Otto Group Purchase - An existing user is able to register
        for a course and make payment for multiple seats in the course using
        the credit card
        """
        multi_seat_user_email = TEST_EMAIL_ACCOUNT.format("+multiseat")
        seat_counter = 3
        # Login to application using the existing credentials
        self.login_user(multi_seat_user_email)
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
        # Go to next page to make the payment
        self.basket.go_to_cybersource_page()
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
            multi_seat_user_email,
            'Order',
            'enrollment_code_csv'
        )
        coupons = self.get_bulk_purchase_enrollment_codes(
            multi_seat_user_email,
            PASSWORD,
            enrollment_file_link
        )
        self.assertEqual(len(coupons), seat_counter)
