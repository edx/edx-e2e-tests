"""
Terms of Service page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.studio import LOGIN_BASE_URL


class TermsOfService(PageObject):
    """
    Terms of Service page
    """
    url = LOGIN_BASE_URL + '/edx-terms-service'

    def is_browser_on_page(self):
        return "Please read these Terms of Service" in self.q(
            css='.content-section'
        ).text[0]
