from e2e_framework.page_object import PageObject
from ..mktg import BASE_URL


class PrivacyPolicyPage(PageObject):
    """
    The Privacy Policy page for the website
    """

    @property
    def name(self):
        return 'mktg.edx_privacy_policy'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/edx-privacy-policy'

    def is_browser_on_page(self):
        return self.browser.title == 'edX Privacy Policy | edX'
