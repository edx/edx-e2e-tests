"""
E2E tests for ORA/LMS integration.
"""

from test_edxapp.base import LoggedInTest
from pages.lms.tab_nav import TabNavPage
from pages.lms.course_nav import CourseNavPage
from pages.lms.open_response import OpenResponsePage


class OpenResponseTest(LoggedInTest):
    """
    Tests that interact with ORA (Open Response Assessment) through the LMS UI.
    """

    # Assume that the user is registered for the demo course
    REGISTER_COURSE_ID = 'edX/Open_DemoX/edx_demo_course'
    REGISTER_COURSE_TITLE = 'Open_DemoX edX Demonstration Course'

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

        # Navigate to the self-assessment problem
        self.ui['lms.dashboard'].view_course(self.REGISTER_COURSE_ID)
        self.ui['lms.tab_nav'].go_to_tab('Courseware')
        self.ui['lms.course_nav'].go_to_section(
            'Example Week 2: Get Interactive', 'Homework - Essays'
        )
        self.ui['lms.course_nav'].go_to_sequential('Self-Assessed Essay')

        # Expect that it's a self-assessment and has the expected essay prompt
        self.assertEqual(self.ui['lms.open_response'].assessment_type, 'self')
        self.assertIn('Censorship in the Libraries', self.ui['lms.open_response'].prompt)

        # Enter a response
        essay = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vehicula."
        self.ui['lms.open_response'].set_response(essay)

        # Save the response and expect some UI feedback
        self.ui['lms.open_response'].save_response()
        self.assertEqual(
            self.ui['lms.open_response'].alert_message,
            "Answer saved, but not yet submitted."
        )

        # Submit the response and expect that we see the self-assessment rubric
        self.ui['lms.open_response'].submit_response()

        # Wait for the rubric to appear
        self.wait_for(lambda: self.ui['lms.open_response'].has_rubric, "rubric to appear")

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
