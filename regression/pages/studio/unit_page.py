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

    def add_word_cloud_component(self):
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
            '.xblock-header-word_cloud', 'Word Cloud Component did not display'
        )
