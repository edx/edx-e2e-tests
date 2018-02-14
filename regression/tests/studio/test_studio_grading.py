"""
Test studio grading
"""
from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.grading_studio import GradingPageExtended
from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.tests.helpers.utils import get_course_info
from regression.tests.helpers.api_clients import StudioLoginApi


class StudioGradingTest(WebAppTest):
    """
    Test studio grading
    """
    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioGradingTest, self).setUp()

        login_api = StudioLoginApi()
        login_api.authenticate(self.browser)

        self.course_info = get_course_info()
        self.grading_page = GradingPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        self.studio_course_outline = CourseOutlinePageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        self.grading_page.visit()

    def test_grade_range(self):
        """
        Verifies default, addition and deletion of grade range
        """
        # Delete any existing grades
        self.grading_page.remove_all_grades()

        # Default
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Addition
        self.grading_page.add_new_grade()
        self.assertEquals(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Verify that after revisiting, changes remain intact
        self.grading_page.visit()
        self.assertEquals(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Deletion
        self.grading_page.remove_grade()
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Verify that after revisiting, changes remain intact
        self.grading_page.visit()
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
