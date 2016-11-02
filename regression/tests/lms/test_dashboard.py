"""
End to end tests for LMS dashboard.
"""
from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.pages.lms.courseware import CoursewarePage
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.tests.helpers.helpers import (
    LoginHelper, get_course_info, get_course_display_name
)
from regression.pages.lms.course_drupal_page import (
    DemoCourseSelectionPage
)
from regression.pages.lms.checkout_page import PaymentPage


class DashboardTest(WebAppTest):
    """
    Regression tests on LMS Dashboard
    """

    def setUp(self):
        super(DashboardTest, self).setUp()
        self.login_page = LmsLogin(self.browser)
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.drupal_course_page = DemoCourseSelectionPage(self.browser)
        self.payment_page = PaymentPage(self.browser)
        LoginHelper.login(self.login_page)

    def test_resume_course(self):
        """
        Verifies that user can successfully resume the course
        """
        course_page = CourseInfoPageExtended(
            self.browser, get_course_info())
        courseware_page = CoursewarePage(self.browser, get_course_info())

        self.dashboard_page.select_course(get_course_display_name())
        course_page.wait_for_page()
        course_page.click_resume_button()
        courseware_page.wait_for_page()
