from bok_choy.web_app_test import WebAppTest
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from edxapp_pages.lms.courseware import CoursewarePage
from regression.tests.helpers import LoginHelper


class DashboardTest(WebAppTest):
    """
    Regression tests on LMS Dashboard
    """
    def setUp(self):
        super(DashboardTest, self).setUp()
        self.login_page = LmsLogin(self.browser)
        LoginHelper.login(self.login_page)
        self.dashboard_page = DashboardPageExtended(self.browser)

    def test_resume_course(self):
        """
        Verifies that we can successfully resume the course
        """
        course_name = 'course-v1:ArbiRaees+AR-1000+fall'
        course_page = CourseInfoPageExtended(self.browser, course_name)
        courseware_page = CoursewarePage(self.browser, course_name)
        self.dashboard_page.select_course('Manual Smoke Test Course 1 - Auto')
        course_page.wait_for_page()
        course_page.click_resume_button()
        courseware_page.wait_for_page()
