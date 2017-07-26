"""
IDP Login page
"""
from bok_choy.page_object import PageObject
from regression.pages.enterprise.enterprise_const import IDP_URL, IDP_NAME


class IDPLogin(PageObject):
    """
    This class handles the IDP login page
    """
    url = IDP_URL

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return IDP_NAME in self.browser.title

    def login_idp_user(self, idp_username, idp_password):
        """
        Login IDP user
        Args:
            idp_username:
            idp_password:
        """
        self.q(css='input[name="j_username"]').fill(idp_username)
        self.q(css='input[name="j_password"]').fill(idp_password)
        self.q(css='input[type="submit"]').click()
