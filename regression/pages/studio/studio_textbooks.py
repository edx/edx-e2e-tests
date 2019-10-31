"""
Extended Textbooks page
"""
from __future__ import absolute_import

from selenium.webdriver.common.action_chains import ActionChains

from edxapp_acceptance.pages.studio.textbook_upload import TextbookUploadPage
from regression.pages import UPLOAD_FILE_DIR
from regression.tests.helpers.utils import get_url


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
        self.q(css='.edit').results[-1].click()
        self.wait_for_element_visibility(
            '.action-add-chapter', 'Text book form'
        )

    def get_textbook_count(self):
        """
        Returns the count of textbooks
        """
        return len(self.q(css='.textbooks-list .textbook'))

    def get_textbook_names(self):
        """
        Returns names of textbooks
        """
        return self.q(css='.textbook-title').text

    def click_delete_button(self):
        """
        Clicks delete
        """
        self.q(css='.delete.action-icon').results[-1].click()
        self.wait_for_element_visibility(
            '#prompt-warning-title', 'Delete pop up box'
        )
        self.q(css='button.action-primary').first.click()
        self.wait_for_element_invisibility(
            '#prompt-warning-title', 'Delete warning box'
        )

    def delete_all_textbooks(self):
        """
        Deletes all textbooks
        """
        while self.get_textbook_count() > 0:
            self.click_delete_button()

    def click_view_live_textbook(self):
        """
        Clicks View Live button on the first textbook available
        """
        button = self.q(css='.view').results[0]
        # This button is hidden, hovering on it makes it visible
        # Using ActionChains to handle this
        ActionChains(
            self.browser
        ).move_to_element(button).click(button).perform()
