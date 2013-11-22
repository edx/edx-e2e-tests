from e2e_framework.page_object import PageObject
from ..cms import BASE_URL


class HowitworksPage(PageObject):
    """
    Home page for Studio when not logged in.
    """

    @property
    def name(self):
        return "cms.howitworks"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + "/howitworks"

    def is_browser_on_page(self):
        return self.browser.title == 'Welcome | edX Studio'
