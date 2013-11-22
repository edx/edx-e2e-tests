from e2e_framework.page_object import PageObject
from ..mktg import BASE_URL


class CourseListPage(PageObject):
    """
    The page on the website for finding courses
    """

    @property
    def name(self):
        return 'mktg.course_list'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/course-list'

    def is_browser_on_page(self):
        return self.is_css_present('div.page-courses-all')
