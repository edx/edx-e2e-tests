"""
Enterprise portal login page
"""
from bok_choy.page_object import PageObject
from regression.pages.enterprise.enterprise_const import (
    ENTERPRISE_NAME,
    ENTERPRISE_PORTAL_LOGIN_URL
)


class EntPortalLogin(PageObject):
    """
    This class handles the IDP login page
    """
    url = ENTERPRISE_PORTAL_LOGIN_URL

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return ENTERPRISE_NAME in self.browser.title

    def login_to_portal(self, username, password):
        """
        Login IDP user
        Arguments:
            username:
            password:
        """
        self.q(css='#__input1-inner[name="username"]').fill(username)
        self.q(css='#__input2-inner[name="password"]').fill(password)
        self.q(css='#__button2').click()
