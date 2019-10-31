"""
LMS Home page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.lms import LOGIN_BASE_URL


class LmsHome(PageObject):
    """
    LMS Home Page
    """
    url = LOGIN_BASE_URL

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return 'Top Institutions' in self.q(css='.hero-large h1').text[0]
