"""
Test studio grading
"""
from uuid import uuid4

from regression.tests.studio.studio_base_test import StudioBaseTestClass
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.grading_studio import GradingPageExtended
from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.tests.helpers import LoginHelper, get_course_info


class StudioGradingTest(StudioBaseTestClass):
    """
    Test studio grading
    """
    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioGradingTest, self).setUp()
        self.login_page = StudioLogin(self.browser)
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

        LoginHelper.login(self.login_page)

        self.grading_page.visit()

    def test_grade_range(self):
        """
        Verifies default, addition and deletion of grade range
        """
        # Default
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Addition
        self.grading_page.click_new_grade_button()
        self.assertEquals(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Verify that after revisiting, changes remain intact
        self.grading_page.visit()
        self.assertEquals(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Deletion
        self.grading_page.click_remove_grade()
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Verify that after revisiting, changes remain intact
        self.grading_page.visit()
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')

    def test_assignment_types(self):
        """
        Verifies that user can add/delete assignment types
        """
        self.grading_page.click_new_assignment_type()
        self.grading_page.fill_assignment_type_fields(
            name='Final',
            abbreviation='Finale',
            total_grade='100',
            total_number='2',
            drop='1'
        )
        self.assertEquals(
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

        # Remove this once addCleanup is added
        # Cleanup Course Outline Page
        self.studio_course_outline.cancel_subsection_settings()
        self.studio_course_outline.delete_section()
        # Cleanup Grading Page
        self.grading_page.visit()
        self.grading_page.delete_assignment_type()
