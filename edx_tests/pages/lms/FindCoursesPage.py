from e2e_framework.PageObject import PageObject
from . import BASE_URL


class FindCoursesPage(PageObject):
    """
    Find courses page (main page of the LMS).
    """

    @property
    def name(self):
        return "lms.find_courses"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL

    def is_browser_on_page(self):
        return self.browser.title == "edX"
