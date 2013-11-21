from e2e_framework.page_object import PageObject
from ..lms import BASE_URL


class CourseInfoPage(PageObject):
    """
    Course info.
    """

    @property
    def name(self):
        return "lms.course_info"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self, course_id=None):
        """
        Go directly to the course info page for `course_id`.
        (e.g. "edX/Open_DemoX/edx_demo_course")
        """
        return BASE_URL + "/courses/" + course_id + "/info"

    def is_browser_on_page(self):
        return self.is_css_present('section.updates')

    def num_updates(self):
        """
        Return the number of updates on the page.
        """
        update_css = 'section.updates ol li'
        return len(self.css_find(update_css))

    def handout_links(self):
        """
        Return a list of handout assets links.
        """
        handouts_css = 'section.handouts ol li a'
        return [el['href'] for el in self.css_find(handouts_css)]
