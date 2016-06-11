"""
End to end tests for Studio Home page
"""
import os
from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.pages.studio.overview import CourseOutlinePage
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.studio_home import DashboardPageExtended


class StudioHomeTest(WebAppTest):
    """
    Test for navigating to the Studio Home page
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    course_id = '/course-v1:ArbiRaees+AR-1000+fall'

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioHomeTest, self).setUp()
        self.studio_login_page = StudioLogin(self.browser)
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = {
            'org': 'ArbiRaees', 'number': 'AR-1000', 'run': 'fall'}

        self.studio_course_outline = CourseOutlinePage(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

    def test_studio_course_select(self):
        """
        Verifies that user can select a course and navigate to its course
        outline page
        """
        self.studio_home_page.visit()
        self.studio_home_page.select_course(
            'Manual Smoke Test Course 1 - Auto')
        self.studio_course_outline.is_browser_on_page()
