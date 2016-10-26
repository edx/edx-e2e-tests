"""
Common features related to course enrollment
"""
import time
import datetime

from regression.pages.common.api_clients import (
    LmsApiClient,
    EnrollmentApiClient
)
from regression.pages.common.utils import read_enrollment_codes_from_text
from regression.pages.ecommerce.basket_page import (
    BasketPage,
    MultiSeatBasketPage
)
from regression.pages.ecommerce.cybersource_page import CyberSourcePage
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.courses_page import CoursesPage
from regression.pages.whitelabel.receipt_page import ReceiptPage
from regression.pages.whitelabel.const import (
    BILLING_INFO,
    PASSWORD,
    PAYMENT_DETAILS,
    TIME_OUT_LIMIT,
    WAIT_TIME
)

from regression.tests.helpers.user_authentication import (
    UserAuthenticationMixin
)


class CourseNotFoundException(Exception):
    """
    Course not found Exception
    """
    pass


class CourseEnrollmentMixin(UserAuthenticationMixin):
    """
    Mixin class for course Enrollment
    """

    def setUp(self):
        """
        Setup for all common features
        """
        super(CourseEnrollmentMixin, self).setUp()
        self.lms_api_client = LmsApiClient()
        self.enrollment_api_client = EnrollmentApiClient()
        # Initialize all page objects
        self.basket = BasketPage(self.browser)
        self.cyber_source = CyberSourcePage(self.browser)
        self.find_courses = CoursesPage(self.browser)
        self.multi_seat_basket = MultiSeatBasketPage(self.browser)
        self.receipt = ReceiptPage(self.browser)
        # Initialize all common variables
        self.course_id = ''
        self.course_title = ''
        self.course_price = 0.0
        self.total_price = 0.0
        self.full_cleanup = True

    def login_and_go_to_basket(self, user_email, bulk_purchase=False):
        """
        Perform all the steps from login to reaching the basket
        If bulk_purchase is set true by test go to multi_seat_basket,
        otherwise go to single_seat_basket
        Args:
            user_email:
            bulk_purchase:
        """
        self.course_about = CourseAboutPage(self.browser, self.course_id)
        self.login_user(user_email)
        # Check that course is not already present on dashboard and use find
        # course link to go to courses page
        self.assertFalse(self.dashboard.is_course_present(self.course_id))
        self.dashboard.go_to_find_courses_page()
        # find the target course and click on it to go to about page
        self.find_courses.go_to_course_about_page(self.course_about)
        # Verify that course price is correct on course about page
        self.assertEqual(self.course_price, self.course_about.course_price)
        if bulk_purchase:
            # go to multi seat basket page
            self.course_about.go_to_multi_seat_basket_page()
        else:
            # go to single seat basket page
            self.course_about.go_to_single_seat_basket_page()
        # Verify course name, course price and total price on basket page
        self.verify_course_name_on_basket()
        self.verify_price_on_basket()

    def pay_with_cybersource(self):
        """
        Make payment using cybersource
        """
        # Go to next page to make the payment
        self.basket.go_to_cybersource_page()
        # Fill out all the billing and payment details and submit the form
        self.otto_payment_using_cyber_source()
        # Application should take user to the receipt page
        # Verify on receipt page that information like course title,
        # course price, total price order date and billing to is
        # displayed correctly
        self.verify_receipt_info()
        self.receipt.go_to_dashboard()

    def assert_enrollment_and_logout(self):
        """
        Verify that course is added to user dashboard and user can access
        the course. After that logout from application
        """
        self.assertTrue(self.is_course_added_to_dashboard())
        self.logout_user_from_lms()

    def assert_enrollment_and_unenroll(self):
        """
        Verify that course is added to user dashboard and user can access
        the course. After that un-enroll from the course
        """
        self.assertTrue(self.is_course_added_to_dashboard())
        self.unenroll_using_ui()

    def otto_payment_using_cyber_source(self):
        """
        Make payment for course by providing Billing Info and Payment details
        in respected areas
        """
        self.cyber_source.set_billing_info(BILLING_INFO)
        self.cyber_source.set_payment_details(PAYMENT_DETAILS)
        self.cyber_source.make_payment(self.receipt)

    def verify_receipt_info(self):
        """
        Verify that Course title on receipt page is correct
        Verify that Course price on receipt page is correct
        Verify that total price on receipt page is correct
        Verify that Order date on receipt page is correct
        """
        self.assertTrue(self.receipt.is_receipt_displayed())
        self.assertIn(self.course_title, self.receipt.order_desc)
        self.assertEqual(
            unicode(datetime.datetime.utcnow().date()),
            self.receipt.order_date
        )
        self.assertEqual(
            [self.receipt.order_amount, self.receipt.total_amount],
            [self.course_price, self.total_price]
        )
        # self.assertIn(self.receipt.billed_to, BILLING_INFO)

    def verify_course_name_on_basket(self):
        """
        Verify that course name is displayed correctly on basket page
        """
        self.assertIn(self.course_title, self.basket.course_name)

    def verify_price_on_basket(self):
        """
        Verify that course price and total price are displayed correctly on
        basket page
        """
        self.assertEqual(
            [self.basket.course_price, self.basket.total_price],
            [self.course_price, self.total_price]
        )

    def verify_item_price_on_multi_seat_basket(self, item_price):
        """
        Verify that item price is displayed correctly on basket page
        :param item_price:
        :return:
        """
        self.assertEqual(self.multi_seat_basket.item_price, item_price)

    def increase_seats(self, additional_seats):
        """
        Increase seat numbers
        :param additional_seats:
        :return:
        """
        self.multi_seat_basket.increase_student_counter(additional_seats)

    def is_course_added_to_dashboard(self):
        """
        Wait for course to appear on dashboard, check by refreshing page a
        couple of time
        Returns:
            True or False
        """
        t_end = time.time() + TIME_OUT_LIMIT
        # Run the loop for a pre defined time
        while time.time() < t_end:
            try:
                if not self.dashboard.is_course_present(self.course_id):
                    raise CourseNotFoundException
                return True
            except CourseNotFoundException:
                time.sleep(WAIT_TIME)
                self.dashboard.visit()

    def get_bulk_purchase_enrollment_codes(
            self,
            user_email,
            password,
            file_url
    ):
        """
        Get bulk purchase enrollment codes from email
        Args:
            user_email:
            password:
            file_url:
        Returns:
            dict containing enrollment codes and urls:
        """
        self.lms_api_client.create_login_session(user_email, password)
        coupons_text = self.lms_api_client.get_coupon_request(file_url)
        return read_enrollment_codes_from_text(coupons_text)


    def unenroll_using_ui(self):
        """
        Un-enroll student from the course
        """
        if not self.dashboard.is_browser_on_page():
            self.dashboard.visit()
        if self.dashboard.is_course_present(self.course_id):
            self.dashboard.unenroll_course(self.course_id)

    def unenroll_using_api(self, user_email, course_id):
        """
        First check if user is enrolled in the course, if so un-enroll
        using api
        Args:
            user_email:
            course_id:
        """
        # Login to lms and get username
        self.lms_api_client.create_login_session(user_email, PASSWORD)
        username = self.lms_api_client.user_name
        # Verify that user is enrolled in the course using enrollment api
        # if enrolled unenroll user using api
        is_enrolled = self.enrollment_api_client.is_user_enrolled(
            username,
            course_id
        )
        if is_enrolled:
            self.lms_api_client.change_enrollment(course_id, 'unenroll')
