"""
Base class for tests with enrollment capability
"""
from __future__ import absolute_import

import datetime

from bok_choy.promise import EmptyPromise
from six import text_type

from regression.pages.whitelabel.basket_page import CyberSourcePage, MultiSeatBasketPage, SingleSeatBasketPage
from regression.pages.whitelabel.const import BILLING_INFO, CARD_HOLDER_INFO, PASSWORD
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.courses_page import CoursesPage
from regression.pages.whitelabel.receipt_page import ReceiptPage
from regression.tests.helpers.api_clients import EnrollmentApiClient, LmsApiClient
from regression.tests.whitelabel.white_label_tests_base import WhiteLabelTestsBaseClass


class CourseNotFoundException(Exception):
    """
    Course not found Exception
    """


class CourseEnrollmentTest(WhiteLabelTestsBaseClass):
    """
    Class for tests with enrollment capability
    """

    def setUp(self):
        super(CourseEnrollmentTest, self).setUp()
        self.lms_api_client = LmsApiClient()
        self.enrollment_api_client = EnrollmentApiClient()
        # Initialize all page objects
        self.cyber_source_page = CyberSourcePage(self.browser)
        self.courses_page = CoursesPage(self.browser)
        self.multi_seat_basket_page = MultiSeatBasketPage(self.browser)
        self.single_seat_basket_page = SingleSeatBasketPage(self.browser)
        self.receipt_page = ReceiptPage(self.browser)

        # Initialize all common variables
        self.course_id = ''
        self.course_title = ''
        self.course_price = 0.0
        self.total_price = 0.0
        self.full_cleanup = True

    def go_to_basket(self, bulk_purchase=False):
        """
        Perform all the steps from dashboard to reaching the basket page.

        If bulk_purchase is set to 'True' then go to multi seat basket,
        otherwise go to single seat basket.

        Arguments:
            bulk_purchase(bool): Indicates type of the purchase.
        """
        course_about_page = CourseAboutPage(self.browser, self.course_id)
        # Check that course is not already present on dashboard and use find
        # course link to go to courses page
        self.assertFalse(self.dashboard_page.is_course_present(self.course_id))
        self.dashboard_page.click_courses_button()
        self.courses_page.wait_for_page()
        # find the target course and click on it to go to about page
        self.courses_page.click_on_the_course(self.course_id)
        course_about_page.wait_for_page()
        # Verify that course price is correct on course about page
        self.assertEqual(
            self.course_price, course_about_page.course_price
        )
        if bulk_purchase:
            # go to multi seat basket page
            course_about_page.click_on_multi_seat_basket()
            self.multi_seat_basket_page.wait_for_page()
        else:
            # go to single seat basket page
            course_about_page.click_on_single_seat_basket()
            self.single_seat_basket_page.wait_for_page()
        # Verify course name, course price and total price on basket page
        # self.verify_course_name_on_basket()
        self.verify_price_on_basket()

    def verify_course_name_on_basket(self):
        """
        Verify that course name is displayed correctly on basket page.
        """
        self.assertIn(self.course_title, self.basket_page.course_name)

    def verify_price_on_basket(self):
        """
        Verify that course price and total price are displayed correctly on
        basket page.
        """
        self.assertEqual(
            [self.basket_page.course_price, self.basket_page.total_price],
            [self.course_price, self.total_price]
        )

    def assert_enrollment_and_logout_of_ecommerce(self):
        """
        Verify that course is added to user dashboard and user can access
        the course. After that, logout from application.
        """
        self.assert_course_added_to_dashboard()
        self.logout_user_from_ecommerce()

    def assert_course_added_to_dashboard(self):
        """
        Waits for course to appear on dashboard.
        """
        def check_course():
            """
            Checks if course is present on dashboard and revisits the page if
            it is not there.
            Returns:
                True: If course present
                False: Otherwise
            """
            if self.dashboard_page.is_course_present(self.course_id):
                return True
            self.dashboard_page.visit()
            return False

        EmptyPromise(
            check_course, 'Course is present on dashboard'
        ).fulfill()

    def otto_payment_using_cyber_source(self):
        """
        Make payment for course by providing Billing Info and Payment details
        in respected areas.
        """
        self.cyber_source_page.set_card_holder_info(CARD_HOLDER_INFO)
        self.cyber_source_page.set_billing_info(BILLING_INFO)
        self.cyber_source_page.click_payment_button()
        self.receipt_page.wait_for_page()

    def unenroll_using_api(self, user_email, course_id):
        """
        Un-enroll user from a course.

        Arguments:
            user_email(str): User's email
            course_id(str): The id of course in which user is enrolled.
        """
        # Login to lms and get username
        self.lms_api_client.create_login_session(user_email, PASSWORD)
        username = self.lms_api_client.user_name
        # Verify that user is enrolled in the course using enrollment api.
        # If enrolled, then un-enroll user using api.
        is_enrolled = self.enrollment_api_client.is_user_enrolled(
            username,
            course_id
        )
        if is_enrolled:
            self.lms_api_client.change_enrollment(course_id, 'unenroll')

    def verify_info_is_populated_on_basket(self, discounted_price):
        """
        After discount redeem url is used verify that following information is
        displayed correctly on basket page:
        i) Coupon is applied
        ii) Discounted amount

        Arguments:
            discounted_price(float): Discounted price of the course.
        """
        self.assertTrue(self.single_seat_basket.is_voucher_applied())
        self.assertEqual(
            self.single_seat_basket.total_price_after_discount,
            discounted_price
        )

    def unenroll_using_ui(self):
        """
        Un-enroll student from the course.
        """
        if not self.dashboard_page.is_browser_on_page():
            self.dashboard_page.visit()
        if self.dashboard_page.is_course_present(self.course_id):
            self.dashboard_page.unenroll_course(self.course_id)

    def assert_enrollment_and_unenroll(self):
        """
        Asserts that course is added to user dashboard and user can access
        the course. After that un-enroll from the course.
        """
        self.assert_course_added_to_dashboard()
        self.unenroll_using_ui()

    def pay_with_cybersource(self):
        """
        Make payment using cybersource.
        """
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Application should take user to the receipt page
        # Verify on receipt page that information like course title,
        # course price, total price order date and billing to is
        # displayed correctly
        self.verify_receipt_info()
        self.receipt_page.click_in_nav_to_go_to_dashboard()

    def verify_receipt_info(self):
        """
        Verify that Course title, Course Price, total price and order date on
        receipt page is correct.
        """
        self.assertIn(self.course_title, self.receipt_page.order_desc)
        self.assertEqual(
            # Slight chance that this will fail if the test execution crosses
            # the boundary of midnight
            text_type(datetime.datetime.utcnow().date()),
            self.receipt_page.order_date
        )
        self.assertEqual(
            [self.receipt_page.order_amount, self.receipt_page.total_amount],
            [self.course_price, self.total_price]
        )
