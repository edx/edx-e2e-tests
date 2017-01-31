"""
Course Schedule and Details Settings page.
"""
from edxapp_acceptance.pages.studio.settings import SettingsPage
from edxapp_acceptance.pages.common.utils import click_css

from regression.pages import UPLOAD_FILE_DIR
from regression.pages.studio.utils import (
    get_course_key,
    click_css_with_animation_enabled
)
from regression.pages.studio import LOGIN_BASE_URL


class SettingsPageExtended(SettingsPage):
    """
    Course Schedule and Details Settings page.
    """

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        course_id = get_course_key(self.course_info)
        return LOGIN_BASE_URL + "/" + self.url_path + "/" + unicode(course_id)

    def upload_course_image(self, file_name):
        """
        Uploads course image without saving it.
        Arguments:
            file_name: file name to be uploaded.
        """
        self.wait_for_element_visibility(
            '#field-course-organization', 'Organization field visibility'
        )
        self.q(css='.wrapper-input button').results[0].click()
        file_input_css = '.upload-dialog input'

        self.wait_for_element_visibility(
            '#modal-window-title', 'Upload Pop up visibility'
        )
        self.browser.execute_script(
            '$("{}").css("display","block");'.format(file_input_css)
        )
        self.q(css=file_input_css).results[0].send_keys(
            UPLOAD_FILE_DIR + "/" + file_name
        )

    def cancel_upload(self):
        """
        Click 'cancel' on the file upload dialog.
        """
        click_css(
            self, '.button.action-cancel', 0, False
        )

    def click_other_settings_links(self, name):
        """
        Clicks links under other course settings as per the 'name' provided
        """
        self.q(css='.nav-related a').filter(lambda el: name in el.text).click()
