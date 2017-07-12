"""
Extended Pages page for a course.
"""
from edxapp_acceptance.pages.common.utils import (
    click_css, sync_on_notification
)
from edxapp_acceptance.tests.helpers import disable_animations
from edxapp_acceptance.pages.studio.utils import drag

from selenium.webdriver.common.action_chains import ActionChains
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
        click_css(
            page=self,
            css='.button.new-button.new-tab',
            source_index=0,
            require_notification=False
        )
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
        click_css(
            page=self,
            css='.action-button-text',
            source_index=index,
            require_notification=False
        )
        self.browser.execute_script(
            'tinyMCE.activeEditor.setContent("{}")'.format(new_content)
        )
        self.browser.execute_script(
            'document.querySelectorAll(".button.action-primary'
            '.action-save")[0].click();'
        )
        sync_on_notification(self)

    def delete_page(self, index=0):
        """
        Deletes the page present at the index passed.

        Arguments:
            index (int): Index of page
        """
        click_css(
            page=self,
            css='.delete-button.action-button',
            source_index=index,
            require_notification=False
        )
        self.q(css='.prompt.warning button.action-primary ').first.click()
        sync_on_notification(self)

    def delete_all_pages(self):
        """
        Deletes all pages.
        """
        while self.get_custom_page_count() > 0:
            self.delete_page()

    def reload_and_wait_for_page(self):
        """
        Reloads and waits for the newly added page to appear.
        """
        self.browser.refresh()
        self.wait_for_the_visibility_of_new_page()

    def wait_for_the_visibility_of_new_page(self):
        """
        Ensures that newly added page is rendered and is visible.
        """
        self.wait_for_element_visibility(
            '.delete-button.action-button', 'Added pages have been loaded.'
        )

    def get_custom_page_count(self):
        """
        Returns the count of custom pages
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
        click_css(
            page=self,
            css='.action-button-text',
            source_index=index,
            require_notification=False
        )
        content = self.browser.execute_script(
            'return tinyMCE.activeEditor.getContent()'
        )
        click_css(
            page=self,
            css='.button.action-cancel',
            source_index=0,
            require_notification=False
        )
        return content

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

    def toggle_wiki_page_display(self):
        """
        Toggles Wiki page display
        """
        disable_animations(self)
        icon_visibility = self.q(
            css='.is-movable[data-tab-id="wiki"] .fa-eye'
        ).visible
        toggle_checkbox_css = '.is-movable[data-tab-id="wiki"] ' \
                              '.toggle-checkbox'

        self.wait_for_element_presence(
            toggle_checkbox_css, 'Toggle button presence'
        )
        checkbox_css_action = self.q(css=toggle_checkbox_css).results[0]
        self.browser.execute_script("arguments[0].click();", checkbox_css_action)
        sync_on_notification(self)
        self.wait_for_ajax()
        if icon_visibility:
            self.wait_for_element_visibility(
                '.is-movable[data-tab-id="wiki"] .fa-eye-slash',
                'Eye icon invisibility'
            )
        else:
            self.wait_for_element_visibility(
                '.is-movable[data-tab-id="wiki"] .fa-eye', 'Icon visibility'
            )

        return 'Wiki'

    def get_all_pages(self):
        """
        Returns all pages
        """
        temp = self.q(css='.course-tab .course-nav-item-header').text

        all_pages = temp + self.q(css='.course-tab .xblock').text
        return all_pages

    def get_all_pages_count(self):
        """
        Returns the count of all pages.
        """
        return len(
            self.q(
                css='.course-tab'
            ).results
        )

    def toggle_wiki_page_show_value(self):
        """
        Toggle Wiki page value if it is configured to show

        Returns:
            bool: True if configured to show otherwise False.
        """
        self.wait_for_element_visibility(
            '.is-movable[data-tab-id="wiki"] .action-visible',
            'Toggle button is visible'
        )
        toggle_value = self.q(
            css='.is-movable[data-tab-id="wiki"] '
                '.action-visible [type="checkbox"]'
        ).results[0].get_attribute('checked')
        if toggle_value:
            return False
        return True

    def drag_and_drop(self, source_index, target_index):
        """
        Drags and drops the page at source_index to the page at target_index

        Args:
            source_index (int):The index of element to be dragged and dropped
            target_index (int):The index element to be dragged and dropped upon
        """
        drag(self, source_index, target_index)
