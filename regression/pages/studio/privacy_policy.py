"""
Privacy Policy page
"""
from bok_choy.page_object import PageObject
from regression.pages.studio import BASE_URL


class PrivacyPolicy(PageObject):
    """
    Terms of Service page
    """
    url = BASE_URL + '/edx-privacy-policy'

    def is_browser_on_page(self):
        return 'edX Privacy Policy' in self.browser.title
