"""
User profile page
"""
from bok_choy.page_object import PageObject

from regression.pages.common.utils import remove_spaces_from_list_elements


class ProfilePage(PageObject):
    """
    Student profile
    """

    url = None

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if profile section is present
        """
        return self.q(
            css=".wrapper-profile-sections.account-settings-container").present

    @property
    def selected_country(self):
        """
        Get selected country name
        Returns:
            selected country:
        """
        return self.q(
            css='#u-field-select-country~.u-field-value-display'
            '>.u-field-value-readonly').text[0]

    @property
    def countries_list(self):
        """
        Get list of all countries
        Returns:
            countries list:
        """
        self.q(
            css='.u-field.u-field-dropdown.u-field-country.'
            'editable-toggle.mode-display'
        ).click()
        self.wait_for_element_presence(
            '.u-field.u-field-dropdown.u-field-country.'
            'editable-toggle.mode-edit',
            'wait for edit mode'
        )
        countries_list_with_spaces = self.q(
            css='select[id="u-field-select-country"] option').text
        return remove_spaces_from_list_elements(countries_list_with_spaces)

    @property
    def selected_language(self):
        """
        Get selected language
        Returns:
            selected language:
        """
        return self.q(
            css='#u-field-select-language_proficiencies~.u-field-value-display'
            '>.u-field-value-readonly'
        ).text[0]

    @property
    def languages_list(self):
        """
        Get list of languages
        Returns:
            languages list
        """
        self.q(
            css='.u-field.u-field-dropdown.u-field-language_proficiencies.'
            'editable-toggle.mode-display'
        ).click()
        self.wait_for_element_presence(
            '.u-field.u-field-dropdown.u-field-language_proficiencies.'
            'editable-toggle.mode-edit',
            'wait for edit mode'
        )
        languages_list_with_spaces = self.q(
            css='select[id="u-field-select-language_proficiencies"] option'
        ).text
        return remove_spaces_from_list_elements(languages_list_with_spaces)
