"""
Unit Page for Studio
"""

from __future__ import absolute_import

from edxapp_acceptance.pages.studio.container import ContainerPage
from edxapp_acceptance.pages.common.utils import disable_animations


class UnitPageExtended(ContainerPage):
    """
    Unit Page for Studio
    """
    def view_live_version(self):
        """
        Clicks View live version button on Units page which opens a new browser
        window and switches the control to the newly opened browser window
        """
        self.q(
            css='.action-button'
            '[title="Open the courseware in the LMS"]'
        ).click()
        self.browser.switch_to_window(self.browser.window_handles[-1])
        self.wait_for_ajax()

    def add_word_cloud_component(self, publish=False):
        """
        Clicks Advanced button in Add New Component then
        Clicks Word Cloud and verifies that it appears on Studio

        """
        add_x_block_button_css = '.add-xblock-component-button' \
                                 '[data-type="advanced"]'
        word_cloud_button_css = '.button-component[data-category="word_cloud"]'

        self.wait_for_element_visibility(
            add_x_block_button_css,
            'Add xblock button is visible.'
        )
        disable_animations(self)
        self.q(css=add_x_block_button_css).click()

        self.wait_for_element_visibility(
            word_cloud_button_css,
            'Word cloud button is visible.'
        )
        self.q(css=word_cloud_button_css).click()
        # Click initiates an ajax call
        self.wait_for_ajax()
        self.wait_for_element_visibility(
            '.xblock-header-word_cloud', 'Word Cloud component displayed'
        )
        if publish:
            self.q(css='.action-publish.action-primary').click()
            # Clicking on the publish button causes an ajax call.
            # We should be waiting for this ajax call to be completed
            # before exiting the function.
            self.wait_for_ajax()

    def add_lti_component(self):
        """
        Clicks Advanced button in Add New Component then
        Clicks LTI and verifies that it appears on Studio
        """
        self.q(
            css='.add-xblock-component-button[data-type="advanced"]'
        ).first.click()
        self.q(css='.button-component[data-category="lti"]').first.click()
        self.wait_for_ajax()
        self.wait_for_element_visibility(
            '.xblock-header-lti', 'Word Cloud Component did not display'
        )

    def add_custom_js_display_and_grading(self):
        """
        Clicks Problem button in Add New Component then
        Advanced button and finally Clicks Custom Javascript Display and
        Grading and verifies that it appears on Studio
        Returns:
            Xblock display name
        """
        self.q(
            css='.add-xblock-component-button[data-type="problem"]'
        ).click()
        advanced_tab_selector = '#ui-id-2'
        custom_js_selector = '.button-component[data-boilerplate=' \
                             '"jsinput_response.yaml"]'
        self.wait_for_element_visibility(
            advanced_tab_selector,
            'Advanced tab is visible.'
        )
        self.q(css=advanced_tab_selector).click()
        self.wait_for_element_visibility(
            custom_js_selector,
            'Custom JavaScript Display and Grading button is visible.'
        )
        self.q(css=custom_js_selector).click()
        self.wait_for_ajax()
        return self.q(css='.xblock-display-name').text[1]
