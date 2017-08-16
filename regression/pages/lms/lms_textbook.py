"""
Textbook page LMS
"""
from bok_choy.page_object import PageObject, unguarded
from regression.pages.lms.utils import workaround_login_redirect


class TextbookPage(PageObject):
    """
    Textbook page LMS
    """
    url = None

    def is_browser_on_page(self):
        return self.q(css='.chapter').visible

    @unguarded
    def visit(self):
        workaround_login_redirect(self)
        super(TextbookPage, self).visit()
