from e2e_framework.PageObject import PageObject
from . import BASE_URL


class DashboardPage(PageObject):
    """
    Student dashboard, where the student can view
    courses she/he has registered for.
    """

    @property
    def name(self):
        return "lms.dashboard"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self, course_id=None):
        return BASE_URL + "/dashboard"

    def is_browser_on_page(self):
        return self.is_css_present('section.my-courses')

    def available_courses(self):
        """
        Return list of the names of available courses.
        e.g. "999 edX Demonstration Course"
        """
        links = self.css_find('section.info > hgroup > h3 > a')
        return [el.text for el in links]
