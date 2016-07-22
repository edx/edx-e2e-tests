"""
Utility functions for studio page objects.
"""
from opaque_keys.edx.locator import CourseLocator
from edxapp_acceptance.pages.common.utils import wait_for_notification


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
    Click the button/link with the given css and index
    on the specified page (subclass of PageObject).

    Will only consider elements that are displayed and
    have a height and width greater than zero.

    If require_notification is False (default value is True),
    the method will return immediately. Otherwise, it will
    wait for the "mini-notification" to appear and disappear.
    """
    def _is_visible(element):
        """Is the given element visible?"""
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
    Ensures that a modal prompt and confirmation button are
    visible, then clicks the button. The prompt is canceled
    iff cancel is True.
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
