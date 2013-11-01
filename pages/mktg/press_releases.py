from e2e_framework.page_object import PageObject
from . import BASE_URL


class PressReleasesPage(PageObject):
    """
    The Press Releases page for the website
    """

    @property
    def name(self):
        return 'mktg.press_releases'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/press-releases'

    def is_browser_on_page(self):
        return self.browser.title == 'Press Releases | edX'
