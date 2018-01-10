"""
End to end tests for Instructor Dashboard.
"""
from unittest import skipIf
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms import LMS_BASE_URL, LMS_STAGE_BASE_URL
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.instructor_dashboard import (
    InstructorDashboardPageExtended
)
from regression.pages.lms.course_page_lms import CourseHomePageExtended
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.utils import get_course_key


class AnalyticsTest(WebAppTest):
    """
    Regression tests on Analytics on Instructor Dashboard
    """

    def setUp(self):
        super(AnalyticsTest, self).setUp()

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        course_info = get_course_info()
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.instructor_dashboard = InstructorDashboardPageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.course_page = CourseHomePageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.dashboard_page.visit()
        self.dashboard_page.select_course(get_course_display_name())
        self.course_page.wait_for_page()
        self.instructor_dashboard.visit()

    @skipIf(
        LMS_BASE_URL != LMS_STAGE_BASE_URL,
        "Url can't be tested on sandbox"
    )  # LT-61
    def test_analytics_link(self):
        """
        Verifies that edX Insights link is clicked and displayed
        """
        self.instructor_dashboard.click_analytics_tab()
        self.assertEquals(
            self.instructor_dashboard.get_insights_title_text(),
            'INSIGHTS'
        )
