"""
Logout page for LMS
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.home_page import HomePage


class LogoutPage(PageObject):
    """
    LMS Logot
    """

    url = None

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if user drop down is present on the page:
        """
        return self.q(css='.user-name').present

    def logout(self):
        """
        Log out from application
        """
        self.q(css='.user-name').click()
        self.wait_for_element_visibility(
            '.user-account li>a[href="/logout"]',
            'wait for user dropdown to expand'
        )
        self.q(css='.user-account li>a[href="/logout"]').click()
        HomePage(self.browser).wait_for_page()


class EcommerceLogoutPage(PageObject):
    """
    E-Commerce Logout
    """

    url = None

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if user drop down is visible on the page:
        """
        return self.q(css='.user-menu').visible

    def logout_from_ecommerce(self):
        """
        Log out from application
        """
        self.q(
            css='.user-menu>.btn.btn-default.dropdown-toggle.'
            'hidden-xs.nav-button'
        ).click()
        self.wait_for_element_visibility(
            '.dropdown-menu',
            'wait for user dropdown to expand'
        )
        self.q(css='.nav-link[href="/logout/"]').click()
        HomePage(self.browser).wait_for_page()
