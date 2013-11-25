from bok_choy.page_object import PageObject
from ..mktg import BASE_URL


class EdxBlogPage(PageObject):
    """
    The edX Blog page
    """

    @property
    def name(self):
        return 'mktg.edx_blog'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/edx-blog'

    def is_browser_on_page(self):
        return self.browser.title == 'edX Blog | edX'
