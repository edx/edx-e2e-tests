"""
End to end tests for LMS dashboard.
"""
from unittest import skipIf

from edxapp_acceptance.pages.lms.courseware import CoursewarePage

from regression.pages.lms import LMS_BASE_URL, LMS_STAGE_BASE_URL
from regression.pages.lms.checkout_page import PaymentPage
from regression.pages.lms.course_drupal_page import (
    DemoCourseSelectionPage
)
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.tests.helpers import BaseTestClass
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)


class DashboardTest(BaseTestClass):
    """
    Regression tests on LMS Dashboard
    """

    def setUp(self):
        super(DashboardTest, self).setUp()

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        self.dashboard_page = DashboardPageExtended(self.browser)
        self.drupal_course_page = DemoCourseSelectionPage(self.browser)
        self.payment_page = PaymentPage(self.browser)
        self.dashboard_page.visit()

    @skipIf(
        LMS_BASE_URL != LMS_STAGE_BASE_URL,
        'There is no resume button on sandbox'
    )  # LT-60
    def test_resume_course(self):
        """
        Verifies that user can successfully resume the course
        """
        course_page = CourseInfoPageExtended(
            self.browser, get_course_info()
        )
        courseware_page = CoursewarePage(self.browser, get_course_info())

        self.dashboard_page.select_course(get_course_display_name())
        course_page.wait_for_page()
        course_page.click_resume_button()
        courseware_page.wait_for_page()
