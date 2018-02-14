"""
Logout Page
"""
from regression.tests.helpers.new_page_object import NewPageObject


class EcommerceLogoutPage(NewPageObject):
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
