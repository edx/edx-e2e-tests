from bok_choy.web_app_test import WebAppTest
from edxapp_pages.lms.course_about import CourseAboutPage
from edxapp_pages.lms.course_info import CourseInfoPage
from edxapp_pages.lms.find_courses import FindCoursesPage
from edxapp_pages.lms.login import LoginPage
from edxapp_pages.lms.progress import ProgressPage
#from edxapp_pages.lms.register import RegisterPage

from ..helpers import visit_all

class PagesTest(WebAppTest):
    """
    Smoke test that we can visit pages in the Demo Course.
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')
    DEMO_COURSE_ID = "edX/Open_DemoX/edx_demo_course"


    def test_course_pages(self):

        # Log in as a student
        login_page = LoginPage(self.browser)
        login_page.visit()
        login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)

        visit_all([
            clz(self.browser, self.DEMO_COURSE_ID)
            for clz in [CourseAboutPage, CourseInfoPage, ProgressPage]
        ])
