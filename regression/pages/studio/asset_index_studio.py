"""
Asset index page
"""
import urllib

from edxapp_acceptance.pages.studio.asset_index import AssetIndexPage
from edxapp_acceptance.pages.common.utils import (
    click_css, sync_on_notification
)

from regression.pages.studio import BASE_URL
from regression.pages.studio.utils import get_course_key


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
        click_css(
            self, '.button.upload-button.new-button', 0, False)
        self.wait_for_element_visibility(
            self.UPLOAD_FORM_CSS, 'New file upload prompt has been opened.')

    @property
    def asset_files_names(self):
        """
        Get the names of uploaded files.
        Returns:
            list: Uploaded files.
        """
        return self.q(css='.assets-table tbody tr .filename').text

    @property
    def asset_files_count(self):
        """
        Returns the count of files uploaded.
        """
        return len(self.q(css='#asset-table-body tr').execute())

    @property
    def asset_delete_links(self):
        """Return a list of WebElements for deleting the assets"""
        css = '.assets-table tbody tr .remove-asset-button'
        return self.q(css=css).execute()

    def asset_locks(self, locked_only=True):
        """
        Return a list of WebElements of the lock checkboxes for assets
        or an empty list if there are none.
        """
        if locked_only:
            css = "li.action-lock input[checked='checked']"
        else:
            css = "li.action-lock input"
        return self.q(css=css).execute()

    def confirm_asset_deletion(self):
        """ Click to confirm deletion and sync on the notification"""
        self.q(css='button.action-primary').click()
        sync_on_notification(self)

    def delete_first_asset(self):
        """ Deletes file then clicks delete on confirmation """
        self.q(css='.remove-asset-button.action-button').first.click()
        self.confirm_asset_deletion()

    def delete_asset_named(self, name):
        """ Delete the asset with the specified name. """
        names = self.asset_files_names
        if name not in names:
            raise LookupError('Asset with filename {} not found.'.format(name))
        delete_links = self.asset_delete_links
        assets = dict(zip(names, delete_links))
        # Now click the link in that row
        assets.get(name).click()
        self.confirm_asset_deletion()

    def delete_all_assets(self):
        """ Delete all uploaded assets """
        while self.asset_files_count:
            self.delete_first_asset()

    def set_asset_lock(self, index=0, lock=True):
        """
        Set the state of the asset in the row specified by index
         to locked or unlocked, depending on the 'lock' flag.
        Note: this will raise an IndexError if the row does not exist
        """
        checkbox = self.q(css="li.action-lock input").execute()[index]
        selected = checkbox.is_selected()
        if (selected and not lock) or (lock and not selected):
            checkbox.click()
        sync_on_notification(self, style='mini')
