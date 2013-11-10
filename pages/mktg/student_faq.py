from e2e_framework.page_object import PageObject
from pages import BASE_URL


class StudentFaqPage(PageObject):
    """
    The FAQ page for the website
    """

    @property
    def name(self):
        return 'mktg.student_faq'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/student-faq'

    def is_browser_on_page(self):
        return self.browser.title == 'Student FAQ | edX'
