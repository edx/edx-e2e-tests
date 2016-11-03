"""
Extended Pages page for a course.
"""
from edxapp_acceptance.pages.common.utils import (
    wait_for_notification,
    click_css)

from regression.pages.studio.course_page_studio import CoursePageExtended


class PagesPageExtended(CoursePageExtended):
    """
    Extended Pages page for a course.
    """
    url_path = "tabs"

    def is_browser_on_page(self):
        return self.q(css='body.view-static-pages').visible

    def add_page(self):
        """
        Adds a new empty page.
        """
        click_css(self, '.button.new-button.new-tab', 0, False)
        self.wait_for_element_visibility(
            '.component.course-tab.is-movable', 'New page is not visible'
        )

    def edit_page(self, new_content, index=0):
        """
        Edits the page present at the index passed.

        Arguments:
            new_content (str): New content to set.
            index (int): Index of page
        """
        click_css(self, '.action-button-text', index, False)
        self.browser.execute_script(
            'tinyMCE.activeEditor.setContent("{}")'.format(new_content)
        )
        self.browser.execute_script(
            'document.querySelectorAll(".button.action-primary'
            '.action-save")[0].click();'
        )
        wait_for_notification(self)

    def delete_page(self, index=0):
        """
        Deletes the page present at the index passed.

        Arguments:
            index (int): Index of page
        """
        click_css(self, '.delete-button.action-button', index, False)
        self.q(css='.prompt.warning button.action-primary ').first.click()
        wait_for_notification(self)

    def reload_and_wait_for_page(self):
        """
        Reloads and waits for the newly added page to appear.
        """
        self.browser.refresh()
        self.wait_for_element_visibility(
            '.delete-button.action-button', 'Added pages have been loaded.'
        )

    def get_page_count(self):
        """
        Get the count of all new pages added.

        Returns:
            int: Count of pages
        """
        return len(self.q(css='.component.course-tab.is-movable'))

    def get_page_content(self, index=0):
        """
        Get the contents of a page present at the index passed.

        Arguments:
            index (int): Index of page
        Returns:
            str: Content of page.
        """
        click_css(self, '.action-button-text', index, False)
        return self.browser.execute_script(
            'return tinyMCE.activeEditor.getContent()'
        )

    def click_view_live_button(self):
        """
        Clicks view live button on pages page and switches to new window
        """
        self.q(css='.view-live-button').click()
        self.browser.switch_to_window(self.browser.window_handles[-1])

    def click_and_verify_see_an_example(self):
        """
        Clicks see an example pop up on pages page and verifies pop up displays
        """
        self.q(css='a[href="#preview-lms-staticpages"]').click()
        self.wait_for_element_visibility(
            'img[alt="Preview of Pages in your course"]', 'Pop up visibility'
        )
