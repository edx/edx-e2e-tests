from e2e_framework.page_object import PageObject
from pages import BASE_URL


class TermsOfServicePage(PageObject):
    """
    The Terms of Service and Honor Code page for the website
    """

    @property
    def name(self):
        return 'mktg.edx_terms_service'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/edx-terms-service'

    def is_browser_on_page(self):
        return self.browser.title == 'edX Terms of Service | edX'
