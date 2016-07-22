"""
Asset index page
"""
import urllib

from edxapp_acceptance.pages.studio.asset_index import AssetIndexPage
from edxapp_acceptance.pages.common.utils import wait_for_notification

from regression.pages.studio.utils import (
    get_course_key,
    click_css_with_animation_enabled,
    confirm_prompt_with_animation_enabled
)
from regression.pages.studio import BASE_URL
from regression.pages import UPLOAD_FILE_DIR


class AssetIndexPageExtended(AssetIndexPage):
    """
    Extended AssetIndex page.
    """
    UPLOAD_FORM_CSS = '.modal-body .title'

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        course_key = get_course_key(self.course_info)
        url = "/".join(
            [BASE_URL, self.url_path, urllib.quote_plus(unicode(course_key))])
        return url if url[-1] is '/' else url + '/'

    def open_upload_file_prompt(self):
        """
        Open new file upload prompt.
        """
        click_css_with_animation_enabled(
            self, '.button.upload-button.new-button', 0, False)
        self.wait_for_element_visibility(
            self.UPLOAD_FORM_CSS, 'New file upload prompt has been opened.')

    def upload_new_file(self, file_names):
        """
        Upload files.
        file_names is a list of the file names we
        want to upload.
        """
        # Make file input field visible.
        file_input_css = '.file-input'
        self.browser.execute_script(
            '$("{}").css("display","block");'.format(file_input_css))
        self.wait_for_element_visibility(
            file_input_css, "Upload button is visible.")
        # Loop through each file and upload.
        for file_name in file_names:
            self.q(css='.file-input').results[0].send_keys(
                UPLOAD_FILE_DIR + "/" + file_name)
            self.wait_for_element_visibility(
                '.progress-bar', 'Upload progress bar is visible.')
            self.wait_for(
                lambda: self.q(
                    css='.progress-fill').text[0] == 'Upload completed',
                description='Upload complete.')
        # Close the upload prompt.
        click_css_with_animation_enabled(self, '.close-button', 0, False)
        self.wait_for_element_invisibility(
            self.UPLOAD_FORM_CSS, 'New file upload prompt has been closed.')

    def get_file_names(self):
        """
        Returns the names of uploaded files.
        """
        return self.q(css='.assets-table tbody tr .title').text

    def delete_file(self, file_indexes):
        """
        Delete the file(s)
        file_indexes is a list of index of files
        we want to delete.
        """
        more_then_one_file = False
        for index in file_indexes:
            if more_then_one_file:
                index = index - 1
            click_css_with_animation_enabled(
                self, '.remove-asset-button.action-button', index, False)
            confirm_prompt_with_animation_enabled(
                self, require_notification=False)
            self.wait_for_notification()
            more_then_one_file = True

    def wait_for_notification(self):
        """
        Waits for the notification to appear and
        disappear on the given page (subclass of PageObject).
        """
        def is_shown():
            """Whether or not the notification is currently showing."""
            return self.q(
                css='.wrapper.wrapper-notification.'
                    'wrapper-notification-confirmation.is-shown').present

        def is_hidden():
            """Whether or not the notification is finished showing."""
            return self.q(
                css='.wrapper.wrapper-notification.'
                    'wrapper-notification-confirmation.is-hiding').present

        self.wait_for(is_shown, 'Notification should have been shown.')
        self.wait_for(is_hidden, 'Notification should have been hidden.')

    def lock_asset(self, index=0):
        """
        Lock the asset present at index passed.
        """
        self.q(
            css='.assets-table tbody tr'
                ' .actions-col .lock-checkbox').results[index].click()
        wait_for_notification(self)

    def sort_assets(self):
        """
        Sort the assets
        """
        click_css_with_animation_enabled(self, '.column-sort-link', 0, False)
