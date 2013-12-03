from bok_choy.page_object import PageObject
from . import BASE_URL


class MediaKitPage(PageObject):
    """
    The Media Kit page for the website
    """

    @property
    def name(self):
        return 'mktg.media_kit'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/media-kit'

    def is_browser_on_page(self):
        return self.browser.title == 'Media Kit | edX'
