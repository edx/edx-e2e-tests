"""
Enterprise Login tests
"""
import os
from bok_choy.web_app_test import WebAppTest
from regression.pages import LOGIN_EMAIL, LOGIN_PASSWORD
from regression.pages.lms import LMS_BASE_URL, LMS_PROTOCOL
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.enterprise.ent_edx_registration_page import (
    EnterpriseEdxRegistration
)
from regression.pages.enterprise.ent_edx_login_page import (
    EnterpriseEdxLogin
)
from regression.pages.enterprise.ent_portal_login_page import (
    EntPortalLogin
)
from regression.pages.enterprise.ent_portal_home_page import (
    EntPortalHome
)
from regression.pages.enterprise.ent_portal_course_page import (
    EntPortalCourseStart,
    EntPortalCourseStructure
)
from regression.pages.enterprise.ent_course_enrollment_page import (
    EntCourseEnrollment
)
from regression.pages.enterprise.user_account import UserAccountSettings
from regression.pages.enterprise.enterprise_const import (
    ENTERPRISE_NAME,
    IDP_CSS_ID
)
from regression.tests.helpers.api_clients import LogoutApi
from regression.tests.helpers.utils import get_random_credentials


class EntTestBase(WebAppTest):
    """
    Test Enterprise Login
    """
    ENT_PORTAL_USERNAME = os.environ.get('ENT_PORTAL_USERNAME')
    ENT_PORTAL_PASSWORD = os.environ.get('ENT_PORTAL_PASSWORD')
    ENT_PORTAL_EDX_LINKED_USERNAME = \
        os.environ.get('ENT_PORTAL_EDX_LINKED_USERNAME')
    ENT_PORTAL_EDX_LINKED_PASSWORD = \
        os.environ.get('ENT_PORTAL_EDX_LINKED_PASSWORD')
    ENT_COURSE_TITLE = os.environ.get('ENT_COURSE_TITLE')
    ENT_COURSE_ORG = os.environ.get('ENT_COURSE_ORG')
    ENT_COURSE_PRICE = os.environ.get('ENT_COURSE_PRICE')
    ENT_COURSE_START_DATE = os.environ.get('ENT_COURSE_START_DATE')

    def setUp(self):
        """
        Initialize all page objects
        """
        super(EntTestBase, self).setUp()
        self.browser.maximize_window()
        self.ent_portal_login = EntPortalLogin(self.browser)
        self.ent_portal_home = EntPortalHome(self.browser)
        self.ent_portal_course_start = \
            EntPortalCourseStart(self.browser)
        self.ent_portal_course_structure = \
            EntPortalCourseStructure(self.browser)
        self.ent_course_enrollment = \
            EntCourseEnrollment(self.browser)
        self.lms_login = LmsLogin(self.browser)
        self.ent_edx_registration = EnterpriseEdxRegistration(self.browser)
        self.ent_edx_login = EnterpriseEdxLogin(self.browser)
        self.dashboard = DashboardPageExtended(self.browser)
        self.user_account = UserAccountSettings(self.browser)

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
        self.assert_(
            self.ENT_COURSE_TITLE in course_title
            for course_title in course_titles
        )
        # Go to course page and then use the link there to go to edX
        self.ent_portal_home.open_enterprise_course_page(
            self.ENT_COURSE_TITLE
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
        logout_api = LogoutApi()
        logout_api.logout_url = '{}://{}/{}'.format(
            LMS_PROTOCOL,
            LMS_BASE_URL,
            'logout'
            )
        logout_api.cookies = self.browser.get_cookies()
        logout_api.logout()

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
            self.ENT_PORTAL_USERNAME,
            self.ENT_PORTAL_PASSWORD)
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
            self.ENT_PORTAL_USERNAME,
            self.ENT_PORTAL_PASSWORD)
        self.access_course()
        self.register_ent_edx_user()
        # Verify that user is on course enrollment page
        self.ent_course_enrollment.wait_for_page()
