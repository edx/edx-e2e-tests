"""
Utility functions for studio page objects.
"""
from opaque_keys.edx.locator import CourseLocator
from edxapp_acceptance.pages.common.utils import click_css
from edxapp_acceptance.tests.helpers import disable_animations
from regression.pages import UPLOAD_FILE_DIR


def get_course_key(course_info, module_store='split'):
    """
    Returns the course key based upon course info passed.
    Course key depends upon the module store passed. The default
    module store is 'split'.
    """
    return CourseLocator(
        course_info['course_org'],
        course_info['course_num'],
        course_info['course_run'],
        deprecated=(module_store == 'draft')
    )


def upload_new_file(page, file_names):
    """
    Upload file(s).

    Arguments:
        page (PageObject): Page to upload file to.
        file_names (list): file name(s) we want to upload.
    """
    # Make file input field visible.
    file_input_css = '.file-input'
    page.browser.execute_script(
        '$("{}").css("display","block");'.format(file_input_css))
    page.wait_for_element_visibility(
        file_input_css, "Upload button is visible.")
    # Loop through each file and upload.
    for file_name in file_names:
        page.q(css=file_input_css).results[0].send_keys(
            UPLOAD_FILE_DIR + "/" + file_name)
        page.wait_for_element_visibility(
            '.progress-bar', 'Upload progress bar is visible.')
        page.wait_for(
            lambda: page.q(
                css='.progress-fill').text[0] == 'Upload completed',
            description='Upload complete.')
    # Close the upload prompt.
    click_css(page, '.close-button', 0, False)
    page.wait_for_element_invisibility(
        page.UPLOAD_FORM_CSS, 'New file upload prompt has been closed.')


def click_confirmation_prompt_primary_button(self):
    """
    Clicks the main action presented by the prompt (such as 'Delete')
    """
    disable_animations(self)
    self.q(css='.prompt button.action-primary').first.click()
    self.wait_for_element_invisibility(
        '.prompt', 'wait for pop up to disappear')
    self.wait_for_ajax()


def get_text(page, css, index=0):
    """
    Get the text inside a DOM element.

    Arguments:
        page (PageObject): page object on which element resides.
        css (str): css of element
        index (int): index position of element.
    """
    return page.q(css=css).text[index]
