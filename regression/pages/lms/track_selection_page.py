"""
Track selection page.
"""
from bok_choy.page_object import PageObject


class TrackSelectionPage(PageObject):
    """
    Track selection page
    """
    url = None

    def is_browser_on_page(self):
        return self.q(
            css='.action-select [value="Audit This Course"]'
        ).visible

    def click_audit_this_course(self):
        """
        Clicks audit this course button after enrolling in a course
        """
        self.q(css='.action-select [value="Audit This Course"]').click()
