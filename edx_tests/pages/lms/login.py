from e2e_framework.page_object import PageObject
from . import BASE_URL


class LoginPage(PageObject):
    """
    Login page for the LMS.
    """

    @property
    def name(self):
        return "lms.login"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + "/login"

    def is_browser_on_page(self):
        page_title = self.css_text('span.title-super').lower()
        return 'log in' in page_title
