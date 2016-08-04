"""
Extended Textbooks page
"""
from edxapp_acceptance.pages.studio.textbook_upload import TextbookUploadPage

from regression.pages import UPLOAD_FILE_DIR
from regression.tests.helpers import get_url


class TextbookPageExtended(TextbookUploadPage):
    """
    Extended Page for textbook page
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return get_url(self.url_path, self.course_info)

    def upload_textbook(self, file_name):
        """
        Uploads a pdf textbook
        """
        self.q(css='.action.action-upload').click()
        self.q(css='.upload-dialog input').results[0].send_keys(
            UPLOAD_FILE_DIR + "/" + file_name)
        self.q(css='.button.action-primary.action-upload').click()
        self.wait_for_element_absence(
            ".modal-window-overlay", "Upload modal closed")

    def click_edit_button(self):
        """
        Clicks edit button
        """
        self.q(css='.edit').click()
        self.wait_for_element_visibility(
            '.action-add-chapter', 'Text book form')

    def click_delete_button(self):
        """
        Clicks delete
        """
        self.q(css='.delete.action-icon').click()
        self.wait_for_element_visibility(
            '#prompt-warning-title', 'Delete pop up box')
        self.q(css='button.action-primary').click()
        self.wait_for_element_invisibility(
            '#prompt-warning-title', 'Delete warning box')
