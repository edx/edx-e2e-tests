"""
Utility functions for studio page objects.
"""
from __future__ import absolute_import

from opaque_keys.edx.locator import CourseLocator

from edxapp_acceptance.pages.common.utils import disable_animations


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
