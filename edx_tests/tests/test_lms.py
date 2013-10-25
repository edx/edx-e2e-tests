"""
E2E tests for the LMS.
"""

from uuid import uuid4

from .base import WebAppTest
from edx_tests.pages.lms.LoginPage import LoginPage
from edx_tests.pages.lms.FindCoursesPage import FindCoursesPage
from edx_tests.pages.lms.InfoPage import InfoPage
from edx_tests.pages.lms.CourseAboutPage import CourseAboutPage
from edx_tests.pages.lms.RegisterPage import RegisterPage
from edx_tests.pages.lms.DashboardPage import DashboardPage


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
        name = self._unique_name()
        self.ui['lms.register'].provide_info(
            name + '@test.com',
            'test_password',
            name,
            name.replace('_', ' ').capitalize()
        )
        self.ui['lms.register'].submit()

        # We should end up at the dashboard
        # Check that we're registered for the course
        course_names = self.ui['lms.dashboard'].available_courses()
        self.assertIn('999 edX Demonstration Course', course_names)

    def _unique_name(self):
        """
        Generate a unique, valid username to avoid conflicts
        between tests.
        """
        return "test_" + str(uuid4())[0:8]

