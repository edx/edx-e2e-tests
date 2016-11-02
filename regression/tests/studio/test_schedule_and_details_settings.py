"""
Regression tests for Studio's Setting page.
"""
from bok_choy.web_app_test import WebAppTest

from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.settings_studio import SettingsPageExtended
from regression.tests.helpers.helpers import LoginHelper, get_course_info

from regression.pages.studio.utils import (
    get_text
)


class ScheduleAndDetailsTest(WebAppTest):
    """
    Tests for Studio's Setting page.
    """
    def setUp(self):
        super(ScheduleAndDetailsTest, self).setUp()
        self.login_page = StudioLogin(self.browser)
        LoginHelper.login(self.login_page)
        self.course_info = get_course_info()

        self.settings_page = SettingsPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.settings_page.visit()

    def test_file_format(self):
        """
        Scenario: Upload course image of a wrong format.

        Given that I am on the Settings page of the course.
        And I click on 'Upload course card image'
        And I upload the image with wrong format.
        Then I should see upload error
        And path in course image input box should not have
        changed.
        """
        # Get current course image.
        current_file = self.settings_page.get_element(
            '.wrapper-input input'
        ).get_attribute('value')
        # Upload the image with wrong format.
        self.settings_page.upload_course_image('README.rst')
        # Assert that error is shown
        self.settings_page.wait_for_element_visibility(
            '.message.message-status.error.is-shown',
            'Error is shown'
        )
        self.assertEqual(
            get_text(
                self.settings_page,
                '.message.message-status.error.is-shown'
            ),
            'Only JPEG or PNG files can be uploaded. '
            'Please select a file ending in .jpeg or .png to upload.'
        )
        self.settings_page.cancel_upload()
        # Assert that file path is unchanged.
        self.assertEqual(
            current_file,
            self.settings_page.get_element(
                '.wrapper-input input'
            ).get_attribute('value')
        )

    def test_cancel_upload(self):
        """
        Scenario: Upload a new course card image but cancel afterwards.

        Given that I am on the Settings page of the course.
        And I click on 'Upload course card image'
        And I upload the image
        And I cancel the image upload.
        And path in course image input box should not have
        changed.
        """
        # Get current course image.
        current_file = self.settings_page.get_element(
            '.wrapper-input input'
        ).get_attribute('value')
        self.settings_page.visit()
        # Upload the image.
        self.settings_page.upload_course_image('Image.png')
        # Cancel the upload
        self.settings_page.cancel_upload()
        # Course card image should be the same as before.
        self.assertEqual(
            current_file,
            self.settings_page.get_element(
                '.wrapper-input input'
            ).get_attribute('value'))
