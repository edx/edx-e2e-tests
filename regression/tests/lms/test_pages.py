"""
End to end test for page's visit.
"""
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.studio.utils import get_course_key
from regression.tests.helpers.utils import get_course_info, visit_all


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

        course_info = get_course_info()
        course_key = get_course_key({
            'course_org': course_info['org'],
            'course_num': course_info['number'],
            'course_run': course_info['run']
        })
        visit_all([
            clz(self.browser, unicode(course_key)) for clz in
            [CourseInfoPageExtended]
        ])
