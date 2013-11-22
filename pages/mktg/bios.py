from e2e_framework.page_object import PageObject
from ..mktg import BASE_URL


class BiosPage(PageObject):
    """
    The Bios page for the website
    """

    @property
    def name(self):
        return 'mktg.bios'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/bios'

    def is_browser_on_page(self):
        return self.browser.title == 'Bios | edX'
