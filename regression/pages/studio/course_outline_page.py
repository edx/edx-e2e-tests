"""
Course Outline Page for Studio
"""

from edxapp_acceptance.pages.studio.overview import CourseOutlinePage
from regression.pages.studio.utils import (
    click_confirmation_prompt_primary_button
)

from regression.tests.helpers import get_url


class CourseOutlinePageExtended(CourseOutlinePage):
    """
    Coure Outline Extended Page for Studio
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return get_url(self.url_path, self.course_info)

    def add_section_with_name(self, text):
        """
        Adds Section clicking the (main) New Section button and given name

        Arguments:
            text (str): The section added will be named to this
        """
        self.q(css='.wrapper-mast nav.nav-actions .button-new').click()
        self.wait_for_ajax()
        self.q(
            css='.incontext-editor-input[value="Section"]'
        ).results[0].send_keys(text)

        self.q(css='.content').first.click()
        # Click initiates an ajax call
        self.wait_for_ajax()

    def add_subsection_with_name(self, text):
        """
        Adds Subsection clicking the subsection button of a section
        There should be one Section available

        Arguments:
            text (str): The sub section added will be named to this
        """
        self.q(css='.button-new[data-default-name="Subsection"]').click()
        self.wait_for_ajax()
        self.q(
            css='.incontext-editor-input[value="Subsection"]'
        ).results[0].send_keys(text)

        self.q(css='.content').first.click()
        # Click initiates an ajax call
        self.wait_for_ajax()

    def add_unit(self):
        """
        Adds Unit clicking the unit button of a sub section
        Navigates to Add Components page
        """
        self.q(css='.button-new[data-default-name="Unit"]').click()

    def get_subsection_grade(self):
        """
        Returns:
        List of grades available in Grade as drop down in subsection settings
        """
        return self.q(css='#grading_type option').text

    def cancel_subsection_settings(self):
        """
        Clicks cancel button of Subsection Settings pop up
        """
        self.q(css='.action-cancel').click()
        self.wait_for_ajax()

    def delete_section(self):
        """
        This deletes a section
        """
        self.q(
            css='.section-header-actions ul.actions-list '
                'li.action-item.action-delete a.delete-button.action-button '
                'span.icon.fa.fa-trash-o'
        ).first.click()
        self.wait_for_ajax()
        click_confirmation_prompt_primary_button(self)
