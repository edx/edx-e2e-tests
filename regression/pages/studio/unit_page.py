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
