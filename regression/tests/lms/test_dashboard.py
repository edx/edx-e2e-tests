"""
End to end tests for LMS dashboard.
"""
from uuid import uuid4
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.course_page_lms import CourseHomePageExtended
from regression.pages.lms.utils import get_course_key
from regression.pages.lms.lms_courseware import CoursewarePageExtended
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)
from regression.tests.helpers.api_clients import (
    StudioLoginApi,
    LmsLoginApi
)
from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)


class DashboardTest(WebAppTest):
    """
    Regression tests on LMS Dashboard
    """

    def setUp(self):
        super(DashboardTest, self).setUp()

        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

        self.studio_home_page = DashboardPageExtended(self.browser)
        self.course_info = get_course_info()
        self.studio_course_outline = CourseOutlinePageExtended(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run']
        )
        self.lms_courseware = CoursewarePageExtended(
            self.browser,
            get_course_key(self.course_info)
        )
        self.course_page = CourseHomePageExtended(
            self.browser, get_course_info()
        )
        self.dashboard_page = DashboardPageExtended(self.browser)

        self.dashboard_page.visit()
