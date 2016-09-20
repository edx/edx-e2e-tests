"""
Unit Page for Studio
"""

from edxapp_acceptance.pages.studio.container import ContainerPage


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

    def get_data_locator(self):
        """
        Returns unique data locator for the component
        """
        data_locator = self.q(
            css='.studio-xblock-wrapper.is-draggable'
        ).attrs('data-locator')[-1]
        return data_locator

    def add_word_cloud_component(self, publish=False):
        """
        Clicks Advanced button in Add New Component then
        Clicks Word Cloud and verifies that it appears on Studio

        """
        self.q(
            css='.add-xblock-component-button[data-type="advanced"]'
        ).click()
        self.q(css='.button-component[data-category="word_cloud"]').click()
        # Click initiates an ajax call
        self.wait_for_ajax()
        self.wait_for_element_visibility(
            '.xblock-header-word_cloud', 'Word Cloud component displayed'
        )
        if publish:
            self.q(css='.action-publish.action-primary').click()
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
        self.q(css='#ui-id-2').click()
        self.q(
            css='.button-component[data-boilerplate="jsinput_response.yaml"]'
        ).click()
        self.wait_for_ajax()
        return self.q(css='.xblock-display-name').text[1]
