"""
Terms of Service page
"""
from bok_choy.page_object import PageObject
from regression.pages.studio import BASE_URL


class TermsOfService(PageObject):
    """
    Terms of Service page
    """
    url = BASE_URL + '/edx-terms-service'

    def is_browser_on_page(self):
        return 'edX Terms of Service' in self.browser.title
