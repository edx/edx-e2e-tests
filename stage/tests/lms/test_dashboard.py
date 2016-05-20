from bok_choy.web_app_test import WebAppTest
from ...pages.lms.login_lms import LmsLogin
from ...pages.lms.dashboard_lms import DashboardPageExtended
from ...pages.lms.course_page_lms import CourseInfoPageExtended
from edxapp_pages.lms.courseware import CoursewarePage
import os

class DashboardTest(WebAppTest):

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        super(DashboardTest, self).setUp()
        self.login_page = LmsLogin(self.browser)
        self.login_page.visit()
        self.login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.dashboard_page = DashboardPageExtended(self.browser)

    def test_resume_course(self):
        self.dashboard_page.select_course()
        course_page = CourseInfoPageExtended(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
        course_page.is_browser_on_page()
        course_page.click_resume_button()
        courseware_page = CoursewarePage(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
        courseware_page.is_browser_on_page()
