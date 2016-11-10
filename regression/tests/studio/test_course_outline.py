"""
End to end tests for Studio Course Outline page
"""
import os
from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.studio.schedule_and_details_page import (
    StudioScheduleDetails
)
from regression.tests.helpers import (
    get_course_info, get_course_display_name
)


class StudioCourseOutlineTest(WebAppTest):
    """
    Test for navigating to the Studio Home page
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioCourseOutlineTest, self).setUp()
        self.studio_login_page = StudioLogin(self.browser)
        self.studio_home_page = DashboardPageExtended(self.browser)
        self.schedule_page = StudioScheduleDetails(self.browser)
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePageExtended(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

        self.studio_home_page.visit()
        self.studio_home_page.select_course(get_course_display_name())
        self.studio_course_outline.wait_for_page()

    def test_edit_start_button(self):
        """
        Verifies that user can click Edit Start Date button and is navigated
        to Schedule and Details page
        """
        self.studio_course_outline.click_edit_start_date_button()
        self.schedule_page.wait_for_page()
