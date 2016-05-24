import os
from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from edxapp_pages.lms.courseware import CoursewarePage


class DashboardTest(WebAppTest):
    """
    Regression tests on LMS Dashboard
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        super(DashboardTest, self).setUp()
        self.login_page = LmsLogin(self.browser)
        self.login_page.visit()
        self.login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.dashboard_page = DashboardPageExtended(self.browser)

    def test_resume_course(self):
        """
        Verifies that we can successfully resume the course
        """
        course_page = CourseInfoPageExtended(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
        courseware_page = CoursewarePage(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
        self.dashboard_page.select_course('Manual Smoke Test Course 1 - Auto')
        course_page.wait_for_page()
        course_page.click_resume_button()
        courseware_page.wait_for_page()
