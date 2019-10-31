"""
Textbook page LMS
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject


class TextbookPage(PageObject):
    """
    Textbook page LMS
    """
    url = None

    def is_browser_on_page(self):
        return self.q(css='.chapter').visible
