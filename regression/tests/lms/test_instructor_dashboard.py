"""
End to end tests for Instructor Dashboard.
"""
from __future__ import absolute_import

from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.course_page_lms import CourseHomePageExtended
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.instructor_dashboard import InstructorDashboardPageExtended
from regression.pages.lms.utils import get_course_key
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_display_name, get_course_info


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
