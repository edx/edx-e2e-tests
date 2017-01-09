"""
Regression tests for Studio's Setting page.
"""
from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.pages.studio.users import UsersPageMixin
from edxapp_acceptance.pages.studio.settings_advanced import (
    AdvancedSettingsPage
)
from edxapp_acceptance.pages.studio.settings_group_configurations import (
    GroupConfigurationsPage
)
from regression.tests.studio.studio_base_test import StudioBaseTestClass
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.settings_studio import SettingsPageExtended
from regression.tests.helpers import LoginHelper, get_course_info
from regression.pages.studio.grading_studio import GradingPageExtended
from regression.pages.studio.utils import (
    get_text
)


class ScheduleAndDetailsTest(StudioBaseTestClass):
    """
    Tests for Studio's Setting page.
    """
    def setUp(self):
        super(ScheduleAndDetailsTest, self).setUp()
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


class ScheduleAndDetailsLinks(WebAppTest):
    """
    Tests for Studio's Setting page links.
    """
    def setUp(self):
        super(ScheduleAndDetailsLinks, self).setUp()
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

    def test_other_grading_link(self):
        """
        Verifies that user can click and navigate to Grading
        """
        name = 'Grading'
        grading_page = GradingPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])
        self.settings_page.click_other_settings_links(name)
        grading_page.wait_for_page()

    def test_other_course_team_link(self):
        """
        Verifies that user can click and navigate to Course Team
        """
        name = 'Course Team'
        course_team_page = UsersPageMixin(self.browser)
        self.settings_page.click_other_settings_links(name)
        course_team_page.wait_for_page()

    def test_other_group_configuration_link(self):
        """
        Verifies that user can click and navigate to Group Configuration
        """
        name = 'Group Configurations'
        group_configuration = GroupConfigurationsPage(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])
        self.settings_page.click_other_settings_links(name)
        group_configuration.wait_for_page()

    def test_other_advanced_settings_link(self):
        """
        Verifies that user can click and navigate to Advanced Settings
        """
        name = 'Advanced Settings'
        advanced_settings = AdvancedSettingsPage(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])
        self.settings_page.click_other_settings_links(name)
        advanced_settings.wait_for_page()
