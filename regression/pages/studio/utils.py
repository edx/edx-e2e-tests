"""
Utility functions for studio page objects.
"""
from opaque_keys.edx.locator import CourseLocator
from edxapp_acceptance.pages.common.utils import wait_for_notification

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


def click_css_with_animation_enabled(page, css, source_index=0,
                                     require_notification=True):
    """
    Clicks element with the given css and index.

    Will only consider elements that are displayed and
    have a height and width greater than zero.

    Arguments:
        page (PageObject): The page on which element resides
        css (str): css of element to be clicked.
        source_index (int): Index of element in case there
            are more than one elements matching the css.
        require_notification (bool): Specifies whether or not
            wait for "mini-notification".
    """
    def _is_visible(element):
        """
        Is the given element visible?
        """
        # Only make the call to size once (instead of
        # once for the height and once for the width)
        # because otherwise you will trigger a extra
        # query on a remote element.
        return element.is_displayed() and all(
            size > 0 for size in element.size.itervalues())

    page.q(css=css).filter(_is_visible).nth(source_index).click()

    if require_notification:
        wait_for_notification(page)

    # Some buttons trigger ajax posts
    # (e.g. .add-missing-groups-button as configured
    # in split_test_author_view.js) so after you click
    # anything wait for the ajax call to finish
    page.wait_for_ajax()


def confirm_prompt_with_animation_enabled(page, cancel=False,
                                          require_notification=None):
    """
    Click the buttons in a modal prompt.

    Ensures that a modal prompt and confirmation buttons are visible,
    then clicks the button.

    Arguments:
        page (PageObject): The page on which prompt is to appear.
        cancel (bool): If True then cancel the prompt.
        require_notification (bool): Specifies whether or not to
            wait for "mini-notification".
    """
    page.wait_for_element_visibility('.prompt', 'Prompt is visible')
    page.wait_for_element_visibility(
        '.wrapper-prompt:focus',
        'Prompt is in focus'
    )
    confirmation_button_css = '.prompt .action-' + (
        'secondary' if cancel else 'primary')
    page.wait_for_element_visibility(
        confirmation_button_css, 'Confirmation button is visible')
    require_notification = (not cancel) \
        if require_notification is None else require_notification
    click_css_with_animation_enabled(
        page, confirmation_button_css,
        require_notification=require_notification)


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
    click_css_with_animation_enabled(page, '.close-button', 0, False)
    page.wait_for_element_invisibility(
        page.UPLOAD_FORM_CSS, 'New file upload prompt has been closed.')


def get_text(page, css, index=0):
    """
    Get the text inside a DOM element.

    Arguments:
        page (PageObject): page object on which element resides.
        css (str): css of element
        index (int): index position of element.
    """
    return page.q(css=css).text[index]
