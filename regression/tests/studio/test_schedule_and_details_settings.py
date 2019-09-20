"""
Regression tests for Studio's Setting page.
"""
from unittest import skip

from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.pages.studio.users import UsersPageMixin
from edxapp_acceptance.pages.studio.settings_advanced import (
    AdvancedSettingsPage
)
from edxapp_acceptance.pages.studio.settings_group_configurations import (
    GroupConfigurationsPage
)
from regression.pages.studio.settings_studio import SettingsPageExtended
from regression.tests.helpers.api_clients import StudioLoginApi
from regression.tests.helpers.utils import get_course_info
from regression.pages.studio.grading_studio import GradingPageExtended
from regression.pages.studio.utils import (
    get_text
)


class ScheduleAndDetailsTest(WebAppTest):
    """
    Tests for Studio's Setting page.
    """
    def setUp(self):
        super(ScheduleAndDetailsTest, self).setUp()

        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)

        self.course_info = get_course_info()

        self.settings_page = SettingsPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.settings_page.visit()

    @skip("Skip test until all cases are discovered")
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

    @skip("Skip test until all cases are discovered")
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
        self.settings_page.upload_course_image('1.png')
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

        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)

        self.course_info = get_course_info()

        self.settings_page = SettingsPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )

        self.grading_page = GradingPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.group_configuration = GroupConfigurationsPage(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.advanced_settings = AdvancedSettingsPage(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.course_team_page = UsersPageMixin(self.browser)

    def test_other_links_crud(self):
        """
        Verifies that user can click and navigate to other links
        Grading: Grading page
        Course team: Course team page
        Group configuration: Group configuration page
        Advanced settings: Advanced settings page
        """
        name_page_dict = {
            'Grading': self.grading_page,
            'Course Team': self.course_team_page,
            'Group Configurations': self.group_configuration,
            'Advanced Settings': self.advanced_settings
        }

        for name, landing_page in name_page_dict.iteritems():
            self.settings_page.visit()
            self.settings_page.click_other_settings_links(name)
            landing_page.wait_for_page()
