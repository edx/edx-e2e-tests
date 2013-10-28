from e2e_framework.page_object import PageObject
from . import BASE_URL


class AboutUsPage(PageObject):
    """
    The About Us page for the website
    """

    @property
    def name(self):
        return 'mktg.about_us'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/about-us'

    def is_browser_on_page(self):
        return self.browser.title == 'About Us | edX'
