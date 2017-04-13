"""
Miscellaneous tests
"""
from regression.pages.whitelabel.const import (
    EXISTING_USER_EMAIL,
    SELECTED_COUNTRY,
    NO_OF_COUNTRIES,
    SAMPLE_COUNTRIES,
    SELECTED_LANGUAGE,
    NO_OF_LANGUAGES,
    SAMPLE_LANGUAGES,
    LOGO_LINK,
    LOGO_ALT_TEXT,
    SOCIAL_MEDIA_LINK
)
from regression.pages.whitelabel.profile_page import ProfilePage
from regression.tests.whitelabel.white_label_tests_base import (
    WhiteLabelTestsBaseClass
)
from regression.pages.whitelabel.const import PASSWORD


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

    def test_verify_social_media_links(self):
        """
        Scenario: To verify that correct social media links are present in
        footer section
        """
        self.home_page.visit()
        self.assertEqual(SOCIAL_MEDIA_LINK, self.home_page.social_links)

    def test_verify_logos(self):
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

    def test_verify_countries_data(self):
        """
        Scenario: To verify that correct countries data is present in user
        profile
        """
        self.login_page.visit()
        self.login_page.provide_info(EXISTING_USER_EMAIL, PASSWORD)
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

    def test_verify_languages_data(self):
        """
        Scenario: To verify that correct languages data is present in user
        profile
        """
        self.login_page.visit()
        self.login_page.provide_info(EXISTING_USER_EMAIL, PASSWORD)
        self.dashboard_page.wait_for_page()
        # Open the profile page
        self.dashboard_page.go_to_profile_page()
        self.profile_page.wait_for_page()
        # Get selected Language and validate it
        self.assertEqual(
            SELECTED_LANGUAGE, self.profile_page.selected_language
        )
        # Get languages list and validate it
        languages = self.profile_page.languages_list
        self.assertEqual(NO_OF_LANGUAGES, len(languages))
        for language in SAMPLE_LANGUAGES:
            self.assertIn(language, languages)
