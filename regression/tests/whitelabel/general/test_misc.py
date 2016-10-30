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
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.profile_page import ProfilePage
from regression.tests.helpers.user_authentication import (
    UserAuthenticationMixin
)


class TestMisc(UserAuthenticationMixin):
    """
    Miscellaneous Tests
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestMisc, self).setUp()
        self.home = HomePage(self.browser)
        self.profile = ProfilePage(self.browser)

    def test_00_verify_social_media_links(self):
        """
        Scenario: To verify that correct social media links are present in
        footer section
        """
        self.home.visit()
        self.assertEqual(SOCIAL_MEDIA_LINK, self.home.social_links)

    def test_01_verify_logos(self):
        """
        Scenario: To verify that correct images are being used for header and
        footer logos
        """
        self.home.visit()
        # Get the link for header logo and verify it
        self.assertIn(LOGO_LINK, self.home.header_logo_link)
        # Get the alt text for header logo and verify it
        self.assertEqual(LOGO_ALT_TEXT, self.home.header_logo_alt_text)
        # Get the link for footer logo and verify it
        self.assertIn(LOGO_LINK, self.home.footer_logo_link)
        # Get the alt text for footer logo and verify it
        self.assertEqual(LOGO_ALT_TEXT, self.home.footer_logo_alt_text)

    def test_02_verify_countries_data(self):
        """
        Scenario: To verify that correct countries data is present in user
        profile
        """
        self.login_user(EXISTING_USER_EMAIL)
        # Open the profile page
        self.dashboard.go_to_profile_page()
        # Get selected country and validate it
        countries = self.profile.countries_list
        self.assertEqual(SELECTED_COUNTRY, self.profile.selected_country)
        self.assertEqual(NO_OF_COUNTRIES, len(countries))
        [self.assertIn(country, countries) for country in SAMPLE_COUNTRIES]

    def test_03_verify_languages_data(self):
        """
        Scenario: To verify that correct languages data is present in user
        profile
        """
        self.login_user(EXISTING_USER_EMAIL)
        # Open the profile page
        self.dashboard.go_to_profile_page()
        # Get selected Language and validate it
        self.assertEqual(SELECTED_LANGUAGE, self.profile.selected_language)
        # Get languages list and validate it
        languages = self.profile.languages_list
        self.assertEqual(SELECTED_LANGUAGE, self.profile.selected_language)
        self.assertEqual(NO_OF_LANGUAGES, len(languages))
        [self.assertIn(language, languages) for language in SAMPLE_LANGUAGES]
