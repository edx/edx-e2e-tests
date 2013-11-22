from e2e_framework.page_object import PageObject
from ..mktg import BASE_URL


class ContactPage(PageObject):
    """
    The Contact Us page for the website
    """

    @property
    def name(self):
        return 'mktg.contact'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/contact-us'

    def is_browser_on_page(self):
        return self.browser.title == 'Contact Us | edX'
