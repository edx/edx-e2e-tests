"""
Course Updates page.
"""
from __future__ import absolute_import

from edxapp_acceptance.pages.common.utils import click_css
from edxapp_acceptance.pages.studio.utils import type_in_codemirror
from regression.pages.studio.course_page_studio import CoursePageExtended


class CourseUpdatesPageExtended(CoursePageExtended):
    """
    Course Updates page.
    """

    url_path = "course_info"

    def is_browser_on_page(self):
        return all([self.q(css='body.view-updates').present,
                    self.q(css='#course-handouts-view .edit-button').visible])

    def open_new_update_form(self):
        """
        Open update form
        """
        self.wait_for_element_visibility(
            '.button.new-button.new-update-button', 'Update form visibility'
        )
        click_css(self, '.button.new-button.new-update-button', 0, False)
        self.wait_for_element_presence(
            '.new-update-form', 'Update form has been opened')

    def write_update_and_save(self, new_update):
        """
        Write new update and save it.
        """
        type_in_codemirror(self, 0, new_update)
        click_css(self, '.save-button', 0, True)
        self.wait_for_element_invisibility(
            '.new-update-form', 'Update form is not visible')

    def edit_course_update(self, course_update_edit_text, index=0):
        """
        Edit course update
        """
        click_css(self, '#course-update-view .edit-button', index, False)
        self.wait_for_element_presence(
            '.new-update-form', 'Update form has been opened')
        self.write_update_and_save(course_update_edit_text)

    def delete_course_update(self, index=0):
        """
        Delete a course update.
        """
        if self.get_course_update_count() > 0:
            click_css(self, '#course-update-view .delete-button', index, False)
            click_css(
                self, '.prompt.warning.has-actions .action-primary', 0, True
            )
            self.wait_for_element_invisibility(
                '.prompt.warning.has-actions .action-primary',
                'Delete prompt is not visible'
            )

    def get_course_update_count(self):
        """
        Get course update count.
        """
        return len(self.q(css='#course-update-view .delete-button').results)

    def delete_all_course_updates(self):
        """
        Delete all course updates.
        """
        while self.get_course_update_count() > 0:
            self.delete_course_update()

    def edit_course_handout(self, update_handout_text):
        """
        Edit course handout.
        """
        click_css(
            self, '#course-handouts-view .edit-button', 0, False)
        self.wait_for_element_visibility(
            '.edit-handouts-form', 'Handout edit form visible.')
        type_in_codemirror(self, 0, update_handout_text)
        click_css(self, '.save-button', 0, True)
        self.wait_for_element_invisibility(
            '.edit-handouts-form', 'Handout edit form is not visible')
