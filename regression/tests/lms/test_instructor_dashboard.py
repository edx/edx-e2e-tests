"""
End to end tests for Instructor Dashboard.
"""
from bok_choy.web_app_test import WebAppTest
from regression.tests.helpers import LoginApi
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.instructor_dashboard import (
    InstructorDashboardPageExtended
)
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.tests.helpers import (
    get_course_info, get_course_display_name
)
from regression.pages.lms.utils import get_course_key


class AnalyticsTest(WebAppTest):
    """
    Regression tests on Analytics on Instructor Dashboard
    """

    def setUp(self):
        super(AnalyticsTest, self).setUp()

        login_app = LoginApi()
        login_app.authenticate(self.browser)

        course_info = get_course_info()
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.instructor_dashboard = InstructorDashboardPageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.course_page = CourseInfoPageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.dashboard_page.visit()
        self.dashboard_page.select_course(get_course_display_name())
        self.course_page.wait_for_page()
        self.instructor_dashboard.visit()

    def test_analytics_link(self):
        """
        Verifies that edX Insights link is clicked and displayed
        """
        self.instructor_dashboard.click_analytics_tab()
        self.assertEquals(
            self.instructor_dashboard.get_insights_title_text(),
            'INSIGHTS'
        )
