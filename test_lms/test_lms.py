"""
E2E tests for the LMS.
"""

from e2e_framework.web_app_test import WebAppTest
from e2e_framework.promise import EmptyPromise, fulfill_before
from credentials import TestCredentials
from fixtures import UserFixture

from pages.lms.login import LoginPage
from pages.lms.find_courses import FindCoursesPage
from pages.lms.info import InfoPage
from pages.lms.course_about import CourseAboutPage
from pages.lms.register import RegisterPage
from pages.lms.dashboard import DashboardPage
from pages.lms.course_info import CourseInfoPage
from pages.lms.tab_nav import TabNavPage
from pages.lms.course_nav import CourseNavPage
from pages.lms.progress import ProgressPage
from pages.lms.video import VideoPage

from .base import LoggedInTest


# The demo course is installed by default in the CI environment
DEMO_COURSE_ID = 'edX/Open_DemoX/edx_demo_course'
DEMO_COURSE_TITLE = 'Open_DemoX edX Demonstration Course'


class RegistrationTest(WebAppTest):
    """
    Verify user-facing pages for unregistered users.
    Test the registration process.
    """

    @property
    def page_object_classes(self):
        return [
            InfoPage, FindCoursesPage, LoginPage,
            CourseAboutPage, RegisterPage, DashboardPage
        ]

    def test_find_courses(self):
        self.ui.visit('lms.find_courses')

    def test_info(self):

        for section_name in InfoPage.sections():
            self.ui.visit('lms.info', section=section_name)

    def test_register(self):

        # Visit the main page with the list of courses
        self.ui.visit('lms.find_courses')

        # Expect that the demo course exists
        course_ids = self.ui['lms.find_courses'].course_id_list()
        self.assertIn(DEMO_COURSE_ID, course_ids)

        # Go to the course about page
        self.ui['lms.find_courses'].go_to_course(DEMO_COURSE_ID)

        # Click the register button
        self.ui['lms.course_about'].register()

        # Fill in registration info and submit
        self.ui['lms.register'].provide_info(TestCredentials())
        self.ui['lms.register'].submit()

        # We should end up at the dashboard
        # Check that we're registered for the course
        course_names = self.ui['lms.dashboard'].available_courses()
        self.assertIn(DEMO_COURSE_TITLE, course_names)


class HighLevelTabTest(LoggedInTest):
    """
    Tests that verify each of the high-level tabs available within a course.
    """

    # Assume that the user is registered for the demo course
    REGISTER_COURSE_ID = DEMO_COURSE_ID
    REGISTER_COURSE_TITLE = DEMO_COURSE_TITLE

    @property
    def page_object_classes(self):
        return (
            super(HighLevelTabTest, self).page_object_classes +
            [CourseInfoPage, TabNavPage, CourseNavPage, ProgressPage, VideoPage]
        )

    def test_course_info(self):
        """
        Navigate to the course info page.
        """
        self.ui['lms.dashboard'].view_course(DEMO_COURSE_ID)

        # Expect just one update
        num_updates = self.ui['lms.course_info'].num_updates()
        self.assertEqual(num_updates, 1)

        # Expect a link to the demo handout pdf
        handout_links = self.ui['lms.course_info'].handout_links()
        self.assertEqual(len(handout_links), 1)
        self.assertIn('demoPDF.pdf', handout_links[0])

    def test_progress(self):
        """
        Navigate to the progress page.
        """
        self.ui['lms.dashboard'].view_course(DEMO_COURSE_ID)
        self.ui['lms.tab_nav'].go_to_tab('Progress')

        # We haven't answered any problems yet, so assume scores are zero
        CHAPTER = 'Example Week 1: Getting Started'
        SECTION = 'Homework - Question Styles'
        EXPECTED_SCORES = [(0, 1), (0, 1), (0, 3), (0, 1), (0, 1), (0, 3), (0, 1)]

        actual_scores = self.ui['lms.progress'].scores(CHAPTER, SECTION)
        self.assertEqual(actual_scores, EXPECTED_SCORES)

    def test_courseware_nav(self):
        """
        Navigate to a particular unit in the courseware.
        """
        self.ui['lms.dashboard'].view_course(DEMO_COURSE_ID)
        self.ui['lms.tab_nav'].go_to_tab('Courseware')

        # Check that the courseware navigation appears correctly
        EXPECTED_SECTIONS = {
            'Introduction': ['Demo Course Overview'],
            'Example Week 1: Getting Started': ['Lesson 1 - Getting Started', 'Homework - Question Styles']
        }
        actual_sections = self.ui['lms.course_nav'].sections
        for section, subsections in EXPECTED_SECTIONS.iteritems():
            self.assertIn(section, actual_sections)
            self.assertEqual(actual_sections[section], EXPECTED_SECTIONS[section])

        # Navigate to a particular section
        self.ui['lms.course_nav'].go_to_section(
            'Example Week 1: Getting Started', 'Homework - Question Styles'
        )

        # Check the sequence items
        EXPECTED_ITEMS = [
            'Pointing on a Picture', 'Drag and Drop', 'Multiple Choice Questions',
            'Mathematical Expressions', 'Chemical Equations', 'Numerical Input', 'Text Input'
        ]

        actual_items = self.ui['lms.course_nav'].sequence_items
        self.assertEqual(len(actual_items), len(EXPECTED_ITEMS))
        for expected in EXPECTED_ITEMS:
            self.assertIn(expected, actual_items)

    def test_video_player(self):
        """
        Play a video in the courseware.
        """

        # Navigate to a video in the demo course
        self.ui['lms.dashboard'].view_course(DEMO_COURSE_ID)
        self.ui['lms.tab_nav'].go_to_tab('Courseware')
        self.ui['lms.course_nav'].go_to_section('Introduction', 'Demo Course Overview')

        # The video should start off paused
        # Since the video hasn't loaded yet, it's elapsed time and duration are both 0
        self.assertFalse(self.ui['lms.video'].is_playing)
        self.assertEqual(self.ui['lms.video'].duration, 0)
        self.assertEqual(self.ui['lms.video'].elapsed_time, 0)

        # Play the video
        self.ui['lms.video'].play()

        # Now we should be playing
        self.assertTrue(self.ui['lms.video'].is_playing)

        # Wait for the video to load the duration
        # We *should* wait for the video's elapsed time to increase,
        # but SauceLabs has difficulty downloading the full video through
        # the ssh tunnel.
        video_duration_loaded = EmptyPromise(
            lambda: self.ui['lms.video'].duration == 194,
            'video has duration', timeout=20
        )

        with fulfill_before(video_duration_loaded):

            # Pause the video
            self.ui['lms.video'].pause()

            # Expect that the elapsed time and duration are reasonable
            # Again, we can't expect the video to actually play because of
            # latency through the ssh tunnel
            self.assertGreaterEqual(self.ui['lms.video'].elapsed_time, 0)
            self.assertEqual(self.ui['lms.video'].duration, 194)

    def _login(self):
        """
        Log in as the test user and navigate to the dashboard,
        where we should see the demo course.
        """
        self.ui.visit('lms.login')
        self.ui['lms.login'].login(self.email, self.password)
        course_names = self.ui['lms.dashboard'].available_courses()
        self.assertIn(DEMO_COURSE_TITLE, course_names)
