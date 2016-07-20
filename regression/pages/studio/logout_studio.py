"""
Logout Page for Studio
"""
from bok_choy.page_object import PageObject
from regression.pages.studio import BASE_URL


class StudioLogout(PageObject):
    """
    Logged Out Page for Studio
    """

    url = BASE_URL

    def is_browser_on_page(self):
        """
        Checks if we are on the correct page
        """
        return self.q(css='.wrapper-text-welcome').present
