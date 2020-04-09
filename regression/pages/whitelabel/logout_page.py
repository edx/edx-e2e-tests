"""
Logout Page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.whitelabel import ECOM_URL_WITH_AUTH


class EcommerceLogoutPage(PageObject):
    """
    E-Commerce Logout
    """

    url = os.path.join(ECOM_URL_WITH_AUTH, 'logout/')

    def logout_from_ecommerce(self):
        """
        Log out from application
        """
        self.visit()
