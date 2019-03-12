"""
End to end tests for submitting a graded problem.
"""
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.course_page_lms import CourseHomePageExtended
from regression.pages.lms.lms_courseware import CoursewarePageExtended
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.utils import get_course_key


class GradedProblemTest(WebAppTest):
    """
    Regression tests on submitting a graded problem
    """

    def setUp(self):
        super(GradedProblemTest, self).setUp()

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        course_info = get_course_info()
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.course_page = CourseHomePageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.lms_courseware = CoursewarePageExtended(
            self.browser,
            get_course_key(course_info)
        )
        self.dashboard_page.visit()
        self.dashboard_page.select_course(get_course_display_name())
        self.course_page.wait_for_page()

    def test_graded_problem(self):
        """
        Verifies submission of a graded problem
        """
        self.course_page.click_resume_button()
        self.lms_courseware.submit_graded_problem()
