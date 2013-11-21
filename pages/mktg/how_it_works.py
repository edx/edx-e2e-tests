from e2e_framework.page_object import PageObject
from ..mktg import BASE_URL


class HowItWorksPage(PageObject):
    """
    The How It Works page on the website
    """

    @property
    def name(self):
        return 'mktg.how_it_works'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/how-it-works'

    def is_browser_on_page(self):
        return self.browser.title == 'How It Works | edX'
