from bok_choy.page_object import PageObject
from ..mktg import BASE_URL


class SchoolsPage(PageObject):
    """
    The page on the website that lists all the partner universities
    """

    @property
    def name(self):
        return 'mktg.schools'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/schools'

    def is_browser_on_page(self):
        return self.browser.title == 'Schools | edX'
