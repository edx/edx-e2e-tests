"""
Miscellaneous tests
"""
from __future__ import absolute_import

from unittest import skipIf

from regression.pages.whitelabel.const import (
    LOGO_ALT_TEXT, LOGO_LINK, NO_OF_COUNTRIES, NO_OF_LANGUAGES,
    ORG, SAMPLE_COUNTRIES, SAMPLE_LANGUAGES, SELECTED_COUNTRY, SOCIAL_MEDIA_LINK
)
from regression.pages.whitelabel.profile_page import ProfilePage
from regression.tests.whitelabel.white_label_tests_base import WhiteLabelTestsBaseClass


class TestMisc(WhiteLabelTestsBaseClass):
    """
    Miscellaneous Tests
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestMisc, self).setUp()
        self.profile_page = ProfilePage(self.browser)

    @skipIf(ORG == 'MITxPRO', 'MITxPRO has no social media links')
    def test_social_media_links(self):
        """
        Scenario: To verify that correct social media links are present in
        footer section
        """
        self.home_page.visit()
        self.assertEqual(SOCIAL_MEDIA_LINK, self.home_page.social_links)

    def test_logos(self):
        """
        Scenario: To verify that correct images are being used for header and
        footer logos
        """
        self.home_page.visit()
        # Get the link for header logo and verify it
        self.assertIn(LOGO_LINK, self.home_page.header_logo_link)
        # Get the alt text for header logo and verify it
        self.assertEqual(LOGO_ALT_TEXT, self.home_page.header_logo_alt_text)
        # Get the link for footer logo and verify it
        self.assertIn(LOGO_LINK, self.home_page.footer_logo_link)
        # Get the alt text for footer logo and verify it
        self.assertEqual(LOGO_ALT_TEXT, self.home_page.footer_logo_alt_text)

    def test_countries_data(self):
        """
        Scenario: To verify that correct countries data is present in user
        profile
        """
        self.register_using_api()
        self.dashboard_page.wait_for_page()
        # Open the profile page
        self.dashboard_page.go_to_profile_page()
        self.profile_page.wait_for_page()
        # Get selected country and validate it
        self.assertEqual(SELECTED_COUNTRY, self.profile_page.selected_country)
        # Get countries list and validate it
        countries = self.profile_page.countries_list
        self.assertEqual(NO_OF_COUNTRIES, len(countries))
        for country in SAMPLE_COUNTRIES:
            self.assertIn(country, countries)

    def test_languages_data(self):
        """
        Scenario: To verify that correct languages data is present in user
        profile
        """
        self.register_using_api()
        self.dashboard_page.wait_for_page()
        # Open the profile page
        self.dashboard_page.go_to_profile_page()
        self.profile_page.wait_for_page()
        # Get languages list and validate it
        languages = self.profile_page.languages_list
        self.assertEqual(NO_OF_LANGUAGES, len(languages))
        for language in SAMPLE_LANGUAGES:
            self.assertIn(language, languages)
