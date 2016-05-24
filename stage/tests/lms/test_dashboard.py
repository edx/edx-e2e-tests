from bok_choy.web_app_test import WebAppTest
from ...pages.lms.lms_login import LmsLoginPage
from ...pages.lms.lms_dashboard import LmsDashboardPage
from ...pages.lms.lms_course_info import LmsCourseInfoPage
from edxapp_pages.lms.courseware import CoursewarePage
from ..helpers import LoginHelper


class DashboardTest(WebAppTest):
    """
    Perform generic tests on dashboard.
    """
    def setUp(self):
        super(DashboardTest, self).setUp()
        login_page = LmsLoginPage(self.browser)
        login_helper = LoginHelper()
        login_helper.login(login_page)
        self.dashboard_page = LmsDashboardPage(self.browser)

    def test_resume_course(self):
        """
        Test that we can successfully resume the course.
        """
        # Select a course from the dashboard.
        self.dashboard_page.select_course()
        course_page = LmsCourseInfoPage(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
        # Confirm that course has been opened.
        course_page.is_browser_on_page()
        # Click resume button
        course_page.click_resume_button()
        courseware_page = CoursewarePage(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
        # Make sure course has been resumed.
        courseware_page.is_browser_on_page()
