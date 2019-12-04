"""
Test studio grading
"""
from __future__ import absolute_import

from uuid import uuid4

from bok_choy.web_app_test import WebAppTest

from regression.pages.studio.course_outline_page import CourseOutlinePageExtended
from regression.pages.studio.grading_studio import GradingPageExtended
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_info


class StudioGradingTest(WebAppTest):
    """
    Test studio grading
    """
    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioGradingTest, self).setUp()

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

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
        self.assertEqual(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Addition
        self.grading_page.add_new_grade()
        self.assertEqual(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Verify that after revisiting, changes remain intact
        self.grading_page.visit()
        self.assertEqual(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Deletion
        self.grading_page.remove_grade()
        self.assertEqual(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Verify that after revisiting, changes remain intact
        self.grading_page.visit()
        self.assertEqual(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')

    def test_assignment_types(self):
        """
        Verifies that user can add/delete assignment types
        """
        # Delete any existing assignment types
        self.grading_page.delete_all_assignment_types()

        self.grading_page.add_new_assignment_type()
        self.grading_page.fill_assignment_type_fields(
            name='Final',
            abbreviation='Finale',
            total_grade='100',
            total_number='2',
            drop='1'
        )
        self.assertEqual(
            self.grading_page.assignment_name_field_value(), ['Final'])

        # Navigating to course outline page to see if the added assignment
        # is available to use on subsections
        self.studio_course_outline.visit()

        section_name = 'Section :{}'.format(uuid4().hex)
        self.studio_course_outline.add_section_with_name(section_name)
        self.assertIn(
            section_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value').text
        )

        subsection_name = 'Subsection :{}'.format(uuid4().hex)
        self.studio_course_outline.add_subsection_with_name(
            subsection_name)
        self.assertIn(
            subsection_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value').text
        )

        self.studio_course_outline.open_subsection_settings_dialog()
        self.assertIn(
            'Final',
            self.studio_course_outline.get_subsection_grade()
        )

        # Delete added section
        self.studio_course_outline.cancel_subsection_settings()
        self.studio_course_outline.delete_section()
        # Delete added assignment type
        self.grading_page.visit()
        self.grading_page.delete_assignment_type()
