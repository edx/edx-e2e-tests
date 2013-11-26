"""
E2E tests for ORA/LMS integration.
"""

from .base import LoggedInTest
from lms.selenium_pages.tab_nav import TabNavPage
from lms.selenium_pages.course_nav import CourseNavPage
from lms.selenium_pages.open_response import OpenResponsePage


class OpenResponseTest(LoggedInTest):
    """
    Tests that interact with ORA (Open Response Assessment) through the LMS UI.
    """

    # Assume that the user is registered for the demo course
    REGISTER_COURSE_ID = 'edX/Open_DemoX/edx_demo_course'
    REGISTER_COURSE_TITLE = 'Open_DemoX edX Demonstration Course'

    def setUp(self):
        """
        Always start in the subsection with open response problems.
        """
        super(OpenResponseTest, self).setUp()

        self.ui['lms.dashboard'].view_course(self.REGISTER_COURSE_ID)
        self.ui['lms.tab_nav'].go_to_tab('Courseware')
        self.ui['lms.course_nav'].go_to_section(
            'Example Week 2: Get Interactive', 'Homework - Essays'
        )

    @property
    def page_object_classes(self):
        return (
            super(OpenResponseTest, self).page_object_classes +
            [TabNavPage, CourseNavPage, OpenResponsePage]
        )

    def test_self_assessment(self):
        """
        Test that the user can self-assess an essay.
        """

        # Navigate to the self-assessment problem and submit an essay
        self.ui['lms.course_nav'].go_to_sequential('Self-Assessed Essay')
        self._submit_essay('self', 'Censorship in the Libraries')

        # Check the rubric categories
        self.assertEqual(
            self.ui['lms.open_response'].rubric_categories,
            ["Writing Applications", "Language Conventions"]
        )

        # Fill in the self-assessment rubric
        self.ui['lms.open_response'].submit_self_assessment([0, 1])

        # Expect that we get feedback
        self.assertEqual(
            self.ui['lms.open_response'].rubric_feedback,
            ['incorrect', 'correct']
        )

    def test_ai_assessment(self):
        """
        Test that a user can submit an essay and receive AI feedback.
        """

        # Navigate to the AI-assessment problem and submit an essay
        self.ui['lms.course_nav'].go_to_sequential('Feedback and AI-"Graded" Essays')
        self._submit_essay('ai', 'Censorship in the Libraries')

        # Expect UI feedback that the response was submitted
        self.assertEqual(
            self.ui['lms.open_response'].grader_status,
            "Your response has been submitted. Please check back later for your grade."
        )

    def _submit_essay(self, expected_assessment_type, expected_prompt):
        """
        Submit an essay and verify that the problem uses
        the `expected_assessment_type` ("self", "ai", or "peer") and
        shows the `expected_prompt` (a string).
        """

        # Check the assessment type and prompt
        self.assertEqual(self.ui['lms.open_response'].assessment_type, expected_assessment_type)
        self.assertIn(expected_prompt, self.ui['lms.open_response'].prompt)

        # Enter a response
        essay = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vehicula."
        self.ui['lms.open_response'].set_response(essay)

        # Save the response and expect some UI feedback
        self.ui['lms.open_response'].save_response()
        self.assertEqual(
            self.ui['lms.open_response'].alert_message,
            "Answer saved, but not yet submitted."
        )

        # Submit the response
        self.ui['lms.open_response'].submit_response()
