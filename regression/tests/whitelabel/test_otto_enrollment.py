"""
Tests for enrollment through Otto
"""

from __future__ import absolute_import

from regression.pages.studio.utils import get_course_key
from regression.pages.whitelabel import (
    COURSE_NUMBER, COURSE_ORG, COURSE_RUN, DEFAULT_COURSE_PRICE
)
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.tests.helpers.utils import get_wl_course_info
from regression.tests.whitelabel.course_enrollment_test import CourseEnrollmentTest


class TestEnrollmentOtto(CourseEnrollmentTest):
    """
    Tests for Otto Enrollment
    """

    def setUp(self):
        """
        Initialize all objects
        """
        super(TestEnrollmentOtto, self).setUp()
        self.course_info = get_wl_course_info(
            org=COURSE_ORG,
            num=COURSE_NUMBER,
            run=COURSE_RUN
        )
        self.course_id = str(get_course_key(self.course_info))
        self.course_title = self.course_info["display_name"]
        self.course_price = DEFAULT_COURSE_PRICE
        self.total_price = DEFAULT_COURSE_PRICE
        # Initialize page objects
        self.course_about = CourseAboutPage(self.browser, self.course_id)

    def test_register_and_select_course(self):
        """
        Scenario: Otto flow - A registered user is able to register, select a
        course and make payment for the course using the credit card
        """
        self.register_using_api()
        self.go_to_basket()
        self.pay_with_cybersource()
        self.dashboard_page.wait_for_page()
        self.assert_course_added_to_dashboard()
