"""
Logout Page
"""
from __future__ import absolute_import

import os
from bok_choy.page_object import PageObject

from regression.pages.whitelabel import ECOM_URL_WITH_AUTH


class EcommerceLogoutPage(PageObject):
    """
    E-Commerce Logout
    """

    url = os.path.join(ECOM_URL_WITH_AUTH, 'logout/')

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if the sign out message is on the page.
        """
        return "you have signed out" in self.browser.page_source.lower()
