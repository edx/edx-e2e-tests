from bok_choy.page_object import PageObject
from ..mktg import BASE_URL


class ResearchPedagogyPage(PageObject):
    """
    The Research & Pedagogy page
    """

    @property
    def name(self):
        return 'mktg.research_pedagogy'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/research-pedagogy'

    def is_browser_on_page(self):
        return self.browser.title == 'Research & Pedagogy | edX'
