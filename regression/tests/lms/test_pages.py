"""
End to end test for page's visit.
"""
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.tests.helpers import LmsLoginApi
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.tests.helpers import visit_all


class PagesTest(WebAppTest):
    """
    E2E test that we can visit pages in the Selected Course.
    """
    def test_course_pages(self):
        """
        Verifies that user can navigate to LMS Pages
        """
        # Log in as a student
        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)
        dashboard_page = DashboardPageExtended(self.browser)
        dashboard_page.visit()

        visit_all([
            clz(self.browser, 'course-v1:ArbiRaees+AR-1000+fall') for clz in
            [CourseInfoPageExtended]
        ])
