"""
Privacy Policy page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.studio import LOGIN_BASE_URL


class PrivacyPolicy(PageObject):
    """
    Terms of Service page
    """
    url = LOGIN_BASE_URL + '/edx-privacy-policy'

    def is_browser_on_page(self):
        return "edX adopted an amended Privacy Policy" in self.q(
            css='.content-section'
        ).text[0]
