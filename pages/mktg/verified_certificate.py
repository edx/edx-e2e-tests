from bok_choy.page_object import PageObject
from ..mktg import BASE_URL


class VerifiedCertificatePage(PageObject):
    """
    The page on the website explaining Verified Certs
    """

    @property
    def name(self):
        return 'mktg.verified_certificate'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/verified-certificate'

    def is_browser_on_page(self):
        return self.browser.title == 'Verified Certificate | edX'
