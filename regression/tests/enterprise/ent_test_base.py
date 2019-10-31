"""
Enterprise Login tests
"""
from __future__ import absolute_import

from datetime import datetime

from bok_choy.web_app_test import WebAppTest

from regression.pages import LOGIN_EMAIL, LOGIN_PASSWORD
from regression.pages.enterprise.course_about_page import CourseAboutPageExtended
from regression.pages.enterprise.ent_course_enrollment_page import EnterpriseCourseEnrollment
from regression.pages.enterprise.ent_data_sharing_consent_page import EnterpriseDataSharingConsentPage
from regression.pages.enterprise.ent_edx_login_page import EnterpriseEdxLogin
from regression.pages.enterprise.ent_edx_registration_page import EnterpriseEdxRegistration
from regression.pages.enterprise.ent_portal_course_page import (
    EnterprisePortalCourseStart,
    EnterprisePortalCourseStructure
)
from regression.pages.enterprise.ent_portal_home_page import EnterprisePortalHome
from regression.pages.enterprise.ent_portal_login_page import EnterprisePortalLogin
from regression.pages.enterprise.enterprise_const import (
    ENT_COURSE_TITLE,
    ENT_PORTAL_PASSWORD,
    ENT_PORTAL_USERNAME,
    ENTERPRISE_NAME,
    IDP_CSS_ID
)
from regression.pages.enterprise.user_account import UserAccountSettings
from regression.pages.lms import LMS_BASE_URL, LMS_PROTOCOL
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.track_selection_page import TrackSelectionPage
from regression.pages.whitelabel.basket_page import CyberSourcePage, SingleSeatBasketPage
from regression.pages.whitelabel.const import BILLING_INFO, CARD_HOLDER_INFO
from regression.pages.whitelabel.courses_page import CoursesPage
from regression.pages.whitelabel.ecommerce_courses_page import EcommerceCoursesPage
from regression.pages.whitelabel.receipt_page import ReceiptPage
from regression.tests.helpers.api_clients import LmsApiClient, LmsLoginApi, LogoutApi
from regression.tests.helpers.utils import get_random_credentials


class EnterpriseTestBase(WebAppTest):
    """
    Test Enterprise Login
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(EnterpriseTestBase, self).setUp()
        self.browser.maximize_window()
        self.ent_portal_login = EnterprisePortalLogin(self.browser)
        self.ent_portal_home = EnterprisePortalHome(self.browser)
        self.ent_portal_course_start = \
            EnterprisePortalCourseStart(self.browser)
        self.ent_portal_course_structure = \
            EnterprisePortalCourseStructure(self.browser)
        self.ent_course_enrollment = \
            EnterpriseCourseEnrollment(self.browser)
        self.ent_data_sharing_consent = \
            EnterpriseDataSharingConsentPage(self.browser)
        self.ecommerce_courses_page = \
            EcommerceCoursesPage(self.browser)
        self.lms_login = LmsLogin(self.browser)
        self.ent_edx_registration = EnterpriseEdxRegistration(self.browser)
        self.ent_edx_login = EnterpriseEdxLogin(self.browser)
        self.dashboard = DashboardPageExtended(self.browser)
        self.courses_page = CoursesPage(self.browser)
        self.course_about_page = CourseAboutPageExtended(self.browser)
        self.track_selection_page = TrackSelectionPage(self.browser)
        self.user_account = UserAccountSettings(self.browser)
        self.cyber_source_page = CyberSourcePage(self.browser)
        self.single_seat_basket = SingleSeatBasketPage(self.browser)
        self.receipt_page = ReceiptPage(self.browser)
        self.lms_api_client = LmsApiClient()
        self.login_api = LmsLoginApi()
        self.logout_api = LogoutApi()

    def unlink_account(self):
        """
        Unlink IDP Account
        This serves as a fixture for unlinked user test case, it unlinks the
        user after running the tests to make sure that the precondition
        of test is true
        """
        # Visit account setting page
        self.user_account.visit()
        self.user_account.switch_account_settings_tabs('accounts-tab')
        # If linked account is found, unlink it
        if self.user_account.is_idp_account_linked(IDP_CSS_ID):
            self.user_account.unlink_idp_account(IDP_CSS_ID)
        # Logout using api
        self.logout_from_lms_using_api()

    def add_recovery_email(self, email):
        """
        Add secondary email address for enterprise learner
        """
        self.user_account.visit()
        self.user_account.fill_secondary_email_field(email)

    def login_to_ent_portal(self, ent_portal_username, ent_portal_password):
        """
        Login to enterprise portal and find the course and click on it
        """
        # Open portal
        self.ent_portal_login.visit()
        # Login
        self.ent_portal_login.login_to_portal(
            ent_portal_username,
            ent_portal_password)
        self.ent_portal_home.wait_for_page()

    def access_course(self):
        """
        Access the course from portal
        """
        # Open the course pop up and look for the desired course
        self.ent_portal_home.open_courses_popup()
        course_titles = self.ent_portal_home.fetch_course_titles_list()
        self.assertTrue(
            ENT_COURSE_TITLE in course_title
            for course_title in course_titles
        )
        # Go to course page and then use the link there to go to edX
        self.ent_portal_home.open_enterprise_course_page(
            ENT_COURSE_TITLE
        )
        self.ent_portal_course_start.wait_for_page()
        self.ent_portal_course_start.start_or_continue_course()
        self.ent_portal_course_structure.wait_for_page()
        self.ent_portal_course_structure.open_course_on_edx()
        # Get handle of newly opened edx window and switch control to it
        edx_window = self.driver.window_handles[1]
        self.driver.switch_to_window(edx_window)

    def login_ent_edx_user(self):
        """
        Login the user using edX customized logistration page
        """

        # edx credentials
        self.ent_edx_login.wait_for_page()
        self.assertEqual(
            ENTERPRISE_NAME,
            self.ent_edx_login.get_enterprise_name()
        )
        self.ent_edx_login.login(
            LOGIN_EMAIL,
            LOGIN_PASSWORD
        )

    def register_ent_edx_user(self):
        """
        Register the enterprise user using edX customized logistration page
        """
        __, email = get_random_credentials()
        self.ent_edx_registration.visit()
        self.assertEqual(
            ENTERPRISE_NAME,
            self.ent_edx_registration.get_enterprise_name()
        )
        self.ent_edx_registration.register(
            email=email,
            full_name='Enterprise Test User',
            country="US"
        )

    def logout_from_lms_using_api(self):
        """
        Get cookies from browser and send these cookie to python request to
        logout using api
        """

        self.logout_api.logout_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'logout'
            )
        self.logout_api.cookies = self.browser.get_cookies()
        self.logout_api.logout()

    def login_user_lms_using_api(self):
        """
        Login user to LMS using login API
        """

        self.login_api.authenticate(self.browser)

    def login_and_go_to_course_enrollment_page(self):
        """
        Flow which covers the user login on enterprise portal, selecting the
        course and then login to edx course enrollment page
        """
        # The edX site is visited just to make sure that when user jumps to
        # edX from portal we don't have to handle authentication popup
        self.lms_login.visit()
        # Enterprise portal flow
        self.login_to_ent_portal(
            ENT_PORTAL_USERNAME,
            ENT_PORTAL_PASSWORD)
        self.access_course()
        self.login_ent_edx_user()
        # Verify that user is on course enrollment page
        self.ent_course_enrollment.wait_for_page()

    def register_and_go_to_course_enrollment_page(self):
        """
        Flow which covers the user login on enterprise portal, selecting the
        course and then register to edx course enrollment page
        """
        # The edX site is visited just to make sure that when user jumps to
        # edX from portal we don't have to handle authentication popup
        self.lms_login.visit()
        # Enterprise portal flow
        self.login_to_ent_portal(
            ENT_PORTAL_USERNAME,
            ENT_PORTAL_PASSWORD)
        self.access_course()
        self.ent_edx_login.wait_for_page()
        self.register_ent_edx_user()
        # Verify that user is on course enrollment page
        self.ent_course_enrollment.wait_for_page()

    def payment_using_cyber_source(self):
        """
        Make payment for course by providing Billing Info and Payment details
        in respected areas.
        """
        self.cyber_source_page.set_card_holder_info(CARD_HOLDER_INFO)
        self.cyber_source_page.set_billing_info(BILLING_INFO)
        self.cyber_source_page.click_payment_button()
        self.receipt_page.wait_for_page()

    def register_edx_user(self):
        """
        Register the user using edX registration page
        """
        username, email = get_random_credentials()
        self.ent_edx_registration.visit()
        self.ent_edx_registration.register(
            email=email,
            full_name='Test User',
            username=username,
            password='test123test',
            country="US"
        )
        self.dashboard.wait_for_page()

    def verify_info_is_populated_on_basket(self, discounted_price):
        """
        After User accept data sharing consent from landing pag
        verify that following information is
        displayed correctly on basket page:
        i) Enterprise offer is applied
        ii) Discounted amount

        Arguments:
            discounted_price(float): Discounted price of the course.
        """
        self.assertTrue(self.single_seat_basket.is_offer_applied())
        self.assertEqual(
            self.single_seat_basket.total_price_after_discount,
            discounted_price
        )
        self.payment_using_cyber_source()

    def verify_receipt_info_for_discounted_course(self):
        """
        Verify that info on receipt page is correct.

        Verify
        i) Course title.
        ii) Order date
        """
        self.assertIn(ENT_COURSE_TITLE, self.receipt_page.order_desc)
        self.assertEqual(
            datetime.utcnow().strftime("%Y-%m-%d"),
            self.receipt_page.order_date
        )
