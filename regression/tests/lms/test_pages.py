from bok_choy.web_app_test import WebAppTest
from edxapp_pages.lms.course_info import CourseInfoPage
from edxapp_pages.lms.progress import ProgressPage
from regression.pages.lms.login_lms import LmsLogin
from regression.test.helpers import visit_all, LoginHelper


class PagesTest(WebAppTest):
    """
    Smoke test that we can visit pages in the Demo Course.
    """
    def test_course_pages(self):

        # Log in as a student
        login_page = LmsLogin(self.browser)
        LoginHelper.login(login_page)

        visit_all([
            clz(self.browser, 'course-v1:ArbiRaees+AR-1000+fall')
            for clz in [CourseInfoPage, ProgressPage]
        ])
