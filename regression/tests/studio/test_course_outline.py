"""
End to end tests for Studio Course Outline page
"""
import os
from edxapp_acceptance.tests.helpers import assert_side_bar_help_link

from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.settings_studio import SettingsPageExtended
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.tests.helpers import BaseTestClass
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)

DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')


class StudioCourseOutlineTest(BaseTestClass):
    """Tests of the Course Outline in Studio."""

    def test_course_outline(self):
        """
        Verifies that user can click Edit Start Date button and is navigated
        to Schedule and Details page, and that the Help link for
        'Learn more about content visibility settings' is working.
        """
        studio_login_page = StudioLogin(self.browser)
        studio_home_page = DashboardPageExtended(self.browser)
        studio_login_page.visit()
        studio_login_page.login(DEMO_COURSE_USER, DEMO_COURSE_PASSWORD)

        course_info = get_course_info()

        studio_course_outline = CourseOutlinePageExtended(
            self.browser, course_info['org'], course_info['number'],
            course_info['run'])

        schedule_page = SettingsPageExtended(
            self.browser, course_info['org'], course_info['number'],
            course_info['run'])

        # Verification only, should be on this page after login.
        studio_home_page.wait_for_page()

        # Navigate to the course's outline page
        studio_home_page.select_course(get_course_display_name())
        studio_course_outline.wait_for_page()

        # First verify the Help link
        expected_href = 'https://edx.readthedocs.io/projects/' \
                        'edx-partner-course-staff/en/latest/' \
                        'developing_course/controlling_content_visibility.html'
        # Assert that help link is correct.
        assert_side_bar_help_link(
            test=self,
            page=studio_course_outline,
            href=expected_href,
            help_text='Learn more about content visibility settings',
            as_list_item=False
        )

        # If the help page is still up (see LT-53), then close it.
        if self.browser.current_url.startswith('https://edx.readthedocs.io'):
            # TODO wrap this in a try/except block or otherwise harden,
            # make sure that you now have an active window (the other one)
            # and it's the right one (i.e. Studio or LMS)
            self.browser.close()  # close only the current window
            self.browser.switch_to_window(self.browser.window_handles[0])

        # Now do the verification for the edit start date button.
        studio_course_outline.click_edit_start_date_button()

        # This wait_for_page will also assert that we are on the correct page.
        schedule_page.wait_for_page()
