"""
Logout Page for Studio
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.studio import LOGIN_BASE_URL


class StudioLogout(PageObject):
    """
    Logged Out Page for Studio
    """

    url = LOGIN_BASE_URL

    def is_browser_on_page(self):
        """
        Checks if we are on the correct page
        """
        return self.q(css='.wrapper-text-welcome').present
