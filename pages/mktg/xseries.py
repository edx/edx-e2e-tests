from bok_choy.page_object import PageObject
from ..mktg import BASE_URL


class XSeriesPage(PageObject):
    """
    The page on the website explaining XSeries
    """

    @property
    def name(self):
        return 'mktg.xseries'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/xseries'

    def is_browser_on_page(self):
        return self.browser.title == 'XSeries | edX'
