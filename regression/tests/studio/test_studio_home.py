"""
End to end tests for Studio Home page
"""
import os

from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.pages.studio.overview import CourseOutlinePage

from regression.pages.studio.studio_home import DashboardPageExtended
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)

from regression.tests.helpers.api_clients import StudioLoginApi


class StudioHomeTest(WebAppTest):
    """
    Test for navigating to the Studio Home page
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioHomeTest, self).setUp()

        login_api = StudioLoginApi()
        login_api.authenticate(self.browser)

        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePage(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

    def test_studio_course_select(self):
        """
        Verifies that user can select a course and navigate to its course
        outline page
        """
        self.studio_home_page.visit()
        self.studio_home_page.select_course(get_course_display_name())
        self.studio_course_outline.wait_for_page()
