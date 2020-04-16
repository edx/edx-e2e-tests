"""
Logout Page
"""
from __future__ import absolute_import

import os
from bok_choy.page_object import PageObject
from selenium.common.exceptions import WebDriverException

from regression.pages.whitelabel import ECOM_URL_WITH_AUTH
from regression.pages.whitelabel.home_page import HomePage


class EcommerceLogoutPage(PageObject):
    """
    E-Commerce Logout

    Use visit() to actually perform the logout.
    """

    url = os.path.join(ECOM_URL_WITH_AUTH, 'logout/')

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if the sign out message is on the page.
        """
        home_page = HomePage(self.browser)

        try:
            return ("you have signed out" in self.browser.page_source.lower()) or \
                home_page.is_browser_on_page()
        except WebDriverException:
            # page is not yet available
            return False
