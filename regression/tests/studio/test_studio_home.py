"""
End to end tests for Studio Home page
"""
import os
from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.pages.studio.overview import CourseOutlinePage
from edxapp_acceptance.pages.lms.courseware import CoursewarePage
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.lms.login_lms import LmsLogin
from regression.tests.helpers import LoginHelper, get_course_info


class StudioHomeTest(WebAppTest):
    """
    Test for navigating to the Studio Home page
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioHomeTest, self).setUp()
        self.studio_login_page = StudioLogin(self.browser)
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePage(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

    def test_studio_course_select(self):
        """
        Verifies that user can select a course and navigate to its course
        outline page
        """
        self.studio_home_page.visit()
        self.studio_home_page.select_course(
            'Manual Smoke Test Course 1 - Auto')
        self.studio_course_outline.wait_for_page()


class StudioLmsTest(WebAppTest):
    """
    Tests that require lms verification with studio
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioLmsTest, self).setUp()
        # Login to Lms first to avoid authentication
        self.login_page = LmsLogin(self.browser)
        LoginHelper.login(self.login_page)

        self.studio_login_page = StudioLogin(self.browser)
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePage(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

    def test_view_live_from_dashboard(self):
        """
        Verifies that user can view live course from studio dashboard
        """
        self.studio_home_page.visit()
        self.studio_home_page.click_view_live_button()
        courseware_page = CoursewarePage(
            self.browser, get_course_info())
        courseware_page.wait_for_page()
