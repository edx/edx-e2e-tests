from bok_choy.page_object import PageObject
from ..mktg import BASE_URL


class OrgFaqPage(PageObject):
    """
    The .org FAQ page for the website
    """

    @property
    def name(self):
        return 'mktg.org_faq'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/org-faq'

    def is_browser_on_page(self):
        return self.browser.title == '.org FAQ | edX'
