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
        super().setUp()

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


class DataDownloadTest(WebAppTest):
    """
    Regression tests on Analytics on Instructor Dashboard
    """

    def setUp(self):
        super().setUp()

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
        self.data_download_section = self.instructor_dashboard.select_data_download()

    def test_generate_grade_report(self):
        """
        Tests the Generate Grade Report task
        """
        initial_reports = self.data_download_section.report_download_links.text
        initial_pending_tasks = self.data_download_section.get_number_of_pending_tasks
        self.data_download_section.generate_grade_report_button.click()
        self.data_download_section.wait_for_available_report()
        final_reports = self.data_download_section.report_download_links.text
        final_pending_tasks = self.data_download_section.get_number_of_pending_tasks
        self.assertGreater(len(final_reports), len(initial_reports))
        self.assertEqual(final_pending_tasks, initial_pending_tasks)
        # checking confirm message in case of success
        confirm_message = self.data_download_section.q(css="#report-request-response.msg-confirm").text[0]
        self.assertTrue(confirm_message)
        # checking error message in case of failure
        error_message = self.data_download_section.q(css="#report-request-response-error.msg-error").text[0]
        self.assertFalse(error_message)

    def test_generate_problem_grade_report(self):
        """
        Tests the Generate Problem Grade Report task
        """
        initial_reports = self.data_download_section.report_download_links.text
        initial_pending_tasks = self.data_download_section.get_number_of_pending_tasks
        self.data_download_section.generate_problem_report_button.click()
        self.data_download_section.wait_for_available_report()
        final_reports = self.data_download_section.report_download_links.text
        final_pending_tasks = self.data_download_section.get_number_of_pending_tasks
        self.assertGreater(len(final_reports), len(initial_reports))
        self.assertEqual(final_pending_tasks, initial_pending_tasks)
        # checking confirm message in case of success
        confirm_message = self.data_download_section.q(css="#report-request-response.msg-confirm").text[0]
        self.assertTrue(confirm_message)
        # checking error message in case of failure
        error_message = self.data_download_section.q(css="#report-request-response-error.msg-error").text[0]
        self.assertFalse(error_message)
