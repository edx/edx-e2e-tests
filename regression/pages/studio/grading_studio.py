"""
Grading Page for Studio
"""

from edxapp_acceptance.pages.studio.settings_graders import GradingPage
from regression.pages.studio.utils import save_changes_popup_for_studio

from regression.tests.helpers.helpers import get_url


class GradingPageExtended(GradingPage):
    """
    Grading Page for Studio
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return get_url(self.url_path, self.course_info)

    def letter_grade(self, selector):
        """
        Returns: first letter of grade range on grading page
        Example: if there are no manually added grades it would
        return Pass, if a grade is added it will return 'A'
        """
        return self.q(css=selector)[0].text

    def click_new_grade_button(self):
        """
        Clicks new grade button
        """
        self.q(css='.new-grade-button').click()
        save_changes_popup_for_studio(self)

    def click_remove_grade(self):
        """
        Clicks remove grade button
        """
        # Button displays after hovering on it
        btn_css = '.remove-button'
        self.browser.execute_script("$('{}').focus().click()".format(btn_css))
        self.wait_for_ajax()
        save_changes_popup_for_studio(self)

    def click_new_assignment_type(self):
        """
        Clicks New Assignment type button on Grading page
        """
        self.q(css='.add-grading-data').click()
        save_changes_popup_for_studio(self)

    def fill_assignment_type_fields(
            self,
            name,
            abbreviation,
            total_grade,
            total_number,
            drop
    ):
        """
        Fills text to Assignment Type fields according to assignment box
        number and text provided

        Arguments:
            name: Assignment Type Name
            abbreviation: Abbreviation
            total_grade: Weight of Total Grade
            total_number: Total Number
            drop: Number of Droppable
        """
        self.q(css='#course-grading-assignment-name').fill(name)
        self.q(css='#course-grading-assignment-shortname').fill(abbreviation)
        self.q(css='#course-grading-assignment-gradeweight').fill(total_grade)
        self.q(
            css='#course-grading-assignment-totalassignments'
        ).fill(total_number)

        self.q(css='#course-grading-assignment-droppable').fill(drop)
        save_changes_popup_for_studio(self)

    def assignment_name_field_value(self):
        """
        Returns: Assignment type field value
        """
        return self.q(css='#course-grading-assignment-name').attrs('value')

    def delete_assignment_type(self):
        """
        Deletes Assignment type
        """
        self.q(css='.remove-grading-data').first.click()
        save_changes_popup_for_studio(self)
