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
from regression.pages.studio.settings_studio import SettingsPageExtended
from regression.tests.helpers.api_clients import StudioLoginApi
from regression.tests.helpers.utils import get_course_info
from regression.pages.studio.grading_studio import GradingPageExtended


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
