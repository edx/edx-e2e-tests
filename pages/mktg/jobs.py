from e2e_framework.page_object import PageObject
from ..mktg import BASE_URL


class JobsPage(PageObject):
    """
    The Jobs page for the website
    """

    @property
    def name(self):
        return 'mktg.jobs'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/jobs'

    def is_browser_on_page(self):
        return self.browser.title == 'Jobs | edX'
