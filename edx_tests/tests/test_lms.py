"""
E2E tests for the LMS.
"""


from .base import WebAppTest, TestCredentials
from edx_tests.pages.lms.login import LoginPage
from edx_tests.pages.lms.find_courses import FindCoursesPage
from edx_tests.pages.lms.info import InfoPage
from edx_tests.pages.lms.course_about import CourseAboutPage
from edx_tests.pages.lms.register import RegisterPage
from edx_tests.pages.lms.dashboard import DashboardPage


class LoggedOutTest(WebAppTest):
    """
    Smoke test for pages in the LMS
    that are visible when logged out.
    """

    @property
    def page_object_classes(self):
        return [
            InfoPage, FindCoursesPage, LoginPage,
            CourseAboutPage, RegisterPage, DashboardPage
        ]

    def setup_app(self):
        pass

    def test_find_courses(self):
        self.ui.visit('lms.find_courses')

    def test_login(self):
        self.ui.visit("lms.login")

    def test_info(self):

        for section_name in InfoPage.sections():
            self.ui.visit('lms.info', section=section_name)

    def test_register(self):

        # Visit the main page with the list of courses
        self.ui.visit('lms.find_courses')

        # Expect that the demo course exists
        course_ids = self.ui['lms.find_courses'].course_id_list()
        self.assertIn('edx/999/2013_Spring', course_ids)

        # Go to the course about page
        self.ui['lms.find_courses'].go_to_course('edx/999/2013_Spring')

        # Click the register button
        self.ui['lms.course_about'].register()

        # Fill in registration info and submit
        self.ui['lms.register'].provide_info(TestCredentials())
        self.ui['lms.register'].submit()

        # We should end up at the dashboard
        # Check that we're registered for the course
        course_names = self.ui['lms.dashboard'].available_courses()
        self.assertIn('999 edX Demonstration Course', course_names)
