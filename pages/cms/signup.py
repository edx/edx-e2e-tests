from e2e_framework.page_object import PageObject
from ..cms import BASE_URL


class SignupPage(PageObject):
    """
    Signup page for Studio.
    """

    @property
    def name(self):
        return "cms.signup"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + "/signup"

    def is_browser_on_page(self):
        return self.browser.title == 'Sign Up | edX Studio'