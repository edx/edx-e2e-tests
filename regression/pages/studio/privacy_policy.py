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
        return "This Privacy Policy will be reviewed" in self.q(
            css='.content-section'
        ).text[0]
