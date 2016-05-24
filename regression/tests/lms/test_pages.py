import os
from bok_choy.web_app_test import WebAppTest
from edxapp_pages.lms.course_info import CourseInfoPage
from edxapp_pages.lms.progress import ProgressPage
from regression.pages.lms.login_lms import LmsLogin
from ..helpers import visit_all


class PagesTest(WebAppTest):
    """
    Smoke test that we can visit pages in the Demo Course.
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def test_course_pages(self):

        # Log in as a student
        login_page = LmsLogin(self.browser)
        login_page.visit()
        login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)

        visit_all([
            clz(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
            for clz in [CourseInfoPage, ProgressPage]
        ])
