"""
Course Schedule and Details Settings page.
"""
from __future__ import absolute_import

from six import text_type

from edxapp_acceptance.pages.common.utils import click_css
from edxapp_acceptance.pages.studio.settings import SettingsPage
from regression.pages import UPLOAD_FILE_DIR
from regression.pages.studio import LOGIN_BASE_URL
from regression.pages.studio.utils import get_course_key


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
        return "/".join((LOGIN_BASE_URL, self.url_path, text_type(course_id)))

    def is_browser_on_page(self):
        return self.q(css='body.view-settings #course-organization').visible \
            and self.q(
                css='#course-organization'
            ).results[0].get_attribute('value')

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
        self.wait_for_element_visibility(file_input_css, "File input visible")
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
