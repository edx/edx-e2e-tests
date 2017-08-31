"""
Enterprise Login tests
"""
import os
from bok_choy.web_app_test import WebAppTest
from regression.pages import LOGIN_EMAIL, LOGIN_PASSWORD
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.enterprise.enterprise_edx_logistration_page import (
    EnterpriseEdxLogistration
)
from regression.pages.enterprise.enterprise_portal_login_page import (
    EnterprisePortalLogin
)
from regression.pages.enterprise.enterprise_portal_home_page import (
    EnterprisePortalHome
)
from regression.pages.enterprise.enterprise_portal_course_page import (
    EnterprisePortalCourseStart,
    EnterprisePortalCourseStructure
)
from regression.pages.enterprise.enterprise_course_enrollment_page import (
    EnterpriseCourseEnrollment
)
from regression.pages.enterprise.user_account import UserAccountSettings
from regression.pages.enterprise.enterprise_const import (
    ENTERPRISE_NAME,
    IDP_CSS_ID
)
from regression.tests.helpers.api_clients import LmsSessionApi
from regression.tests.helpers.utils import get_random_credentials


class EnterpriseTestBase(WebAppTest):
    """
    Test Enterprise Login
    """
    ENT_PORTAL_USERNAME = os.environ.get('ENT_PORTAL_USERNAME')
    ENT_PORTAL_PASSWORD = os.environ.get('ENT_PORTAL_PASSWORD')
    ENT_COURSE_TITLE = os.environ.get('ENT_COURSE_TITLE')
    ENT_COURSE_ORG = os.environ.get('ENT_COURSE_ORG')
    ENT_COURSE_PRICE = os.environ.get('ENT_COURSE_PRICE')
    ENT_COURSE_START_DATE = os.environ.get('ENT_COURSE_START_DATE')

    def setUp(self):
        """
        Initialize all page objects
        """
        super(EnterpriseTestBase, self).setUp()
        self.browser.maximize_window()
        self.enterprise_portal_login = EnterprisePortalLogin(self.browser)
        self.enterprise_portal_home = EnterprisePortalHome(self.browser)
        self.enterprise_portal_course_start = \
            EnterprisePortalCourseStart(self.browser)
        self.enterprise_portal_course_structure = \
            EnterprisePortalCourseStructure(self.browser)
        self.enterprise_course_enrollment = \
            EnterpriseCourseEnrollment(self.browser)
        self.lms_login = LmsLogin(self.browser)
        self.enterprise_edx_logistration = \
            EnterpriseEdxLogistration(self.browser)
        self.dashboard = DashboardPageExtended(self.browser)
        self.user_account = UserAccountSettings(self.browser)

    def login_and_unlink_account(self):
        """
        Unlink IDP Account
        This serves as a fixture for unlinked user test case, it unlinks the
        user before running the tests to make sure that the precondition
        of test is true
        """
        # Login using api and transfer session to browser
        lms_login_api = LmsSessionApi('/account/settings')
        lms_login_api.authenticate(self.browser)
        # Visit account setting page
        # self.user_account.visit()
        self.user_account.switch_account_settings_tabs('accounts-tab')
        # If linked account is found, unlink it
        if self.user_account.is_idp_account_linked(IDP_CSS_ID):
            self.user_account.unlink_idp_account(IDP_CSS_ID)
        # Delete all cookies to simulate logout behavior
        lms_login_api.logout()

    def login_to_enterprise_portal(self):
        """
        Login to enterprise portal and find the course and click on it
        """
        # Open portal
        self.enterprise_portal_login.visit()
        # Login
        self.enterprise_portal_login.login_to_portal(
            self.ENT_PORTAL_USERNAME,
            self.ENT_PORTAL_PASSWORD)
        self.enterprise_portal_home.wait_for_page()

    def access_course(self):
        """
        Access the course from portal
        """
        # Open the course pop up and look for the desired course
        self.enterprise_portal_home.open_courses_popup()
        course_titles = self.enterprise_portal_home.fetch_course_titles_list()
        self.assert_(
            self.ENT_COURSE_TITLE in course_title
            for course_title in course_titles
        )
        # Go to course page and then use the link there to go to edX
        self.enterprise_portal_home.open_enterprise_course_page(
            self.ENT_COURSE_TITLE
        )
        self.enterprise_portal_course_start.wait_for_page()
        self.enterprise_portal_course_start.start_or_continue_course()
        self.enterprise_portal_course_structure.wait_for_page()
        self.enterprise_portal_course_structure.open_course_on_edx()
        # Get handle of newly opened edx window and switch control to it
        edx_window = self.driver.window_handles[1]
        self.driver.switch_to_window(edx_window)

    def login_enterprise_edx_user(self):
        """
        Login the user using edX customized logistration page
        """
        # On the logistration page switch to login form and then login with
        # edx credentials
        self.enterprise_edx_logistration.wait_for_page()
        self.assertEqual(
            ENTERPRISE_NAME,
            self.enterprise_edx_logistration.get_enterprise_name()
        )
        # Get the current form and if currently registration page is shown
        # toggle to display login page
        if self.enterprise_edx_logistration.current_form == 'register':
            self.enterprise_edx_logistration.toggle_form()
        self.enterprise_edx_logistration.login(
            LOGIN_EMAIL,
            LOGIN_PASSWORD
        )

    def register_enterprise_edx_user(self):
        """
        Register the enterprise user using edX customized logistration page
        """
        username, email = get_random_credentials()
        self.enterprise_edx_logistration.wait_for_page()
        self.assertEqual(
            ENTERPRISE_NAME,
            self.enterprise_edx_logistration.get_enterprise_name()
        )
        # Get the current form and if currently registration page is not shown
        # toggle to display register page
        if self.enterprise_edx_logistration.current_form != 'register':
            self.enterprise_edx_logistration.toggle_form()
        self.enterprise_edx_logistration.register(
            email=email,
            username=username,
            full_name='Enterprise Test User',
            country="US",
            terms_of_service=True
        )
