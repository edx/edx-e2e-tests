"""
Helpful base test case classes for testing the LMS.
"""

from bok_choy.web_app_test import WebAppTest
from .fixtures import UserFixture
from pages.lms.login import LoginPage
from pages.lms.dashboard import DashboardPage


class LoggedInTest(WebAppTest):
    """
    Tests that assume the user is logged in to a unique account
    and is registered for a course.
    """

    # Subclasses override these to register the user for a course.
    # If not provided, then skip registration.
    REGISTER_COURSE_ID = None
    REGISTER_COURSE_TITLE = None

    @property
    def page_object_classes(self):
        return [LoginPage, DashboardPage]

    @property
    def fixtures(self):
        """
        Create a user account so we can log in.
        The user account is automatically registered for a course.
        """
        self.username = 'test_' + self.unique_id
        self.email = '{0}@example.com'.format(self.username)
        self.password = 'password'

        return [UserFixture(self.username, self.email, self.password, course=self.REGISTER_COURSE_ID)]

    def setUp(self):
        """
        Each test begins after registering for a course and logging in.
        """
        super(LoggedInTest, self).setUp()
        self._login()

    def _login(self):
        """
        Log in as the test user and navigate to the dashboard,
        where we should see the demo course.
        """
        self.ui.visit('lms.login')
        self.ui['lms.login'].login(self.email, self.password)

        if self.REGISTER_COURSE_TITLE is not None:
            course_names = self.ui['lms.dashboard'].available_courses()
            self.assertIn(self.REGISTER_COURSE_TITLE, course_names)
