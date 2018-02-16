"""
Privacy Policy page
"""
from bok_choy.page_object import PageObject
from regression.pages.studio import LOGIN_BASE_URL


class PrivacyPolicy(PageObject):
    """
    Terms of Service page
    """
    url = LOGIN_BASE_URL + '/edx-privacy-policy'

    def is_browser_on_page(self):
        # Temporary condition for Acquia issue
        return ('Web Site Not Found' in self.browser.title or
                "As used in this Privacy Policy" in self.q(
                    css='.field-page-body'
                ).text[0])
