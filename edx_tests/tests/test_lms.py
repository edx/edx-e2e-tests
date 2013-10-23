"""
E2E tests for the LMS.
"""

from .base import WebAppTest
from edx_tests.pages.lms.LoginPage import LoginPage
from edx_tests.pages.lms.FindCoursesPage import FindCoursesPage
from edx_tests.pages.lms.InfoPage import InfoPage


class LoggedOutTest(WebAppTest):
    """
    Smoke test for pages in the LMS
    that are visible when logged out.
    """

    @property
    def page_object_classes(self):
        return [InfoPage, FindCoursesPage, LoginPage]

    def setup_app(self):
        pass

    def test_find_courses(self):
        self.ui.visit('lms.find_courses')

    def test_login(self):
        self.ui.visit("lms.login")

    def test_info(self):

        for section_name in InfoPage.sections():
            self.ui.visit('lms.info', section=section_name)
