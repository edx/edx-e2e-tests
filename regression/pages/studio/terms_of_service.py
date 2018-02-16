"""
Terms of Service page
"""
from bok_choy.page_object import PageObject
from regression.pages.studio import LOGIN_BASE_URL


class TermsOfService(PageObject):
    """
    Terms of Service page
    """
    url = LOGIN_BASE_URL + '/edx-terms-service'

    def is_browser_on_page(self):
        # Temporary condition for Acquia issue
        return ('Web Site Not Found' in self.browser.title or
                "Please read these Terms of Service" in self.q(
                    css='.content-section'
                ).text[0])
