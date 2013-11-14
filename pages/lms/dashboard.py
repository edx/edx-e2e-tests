from e2e_framework.page_object import PageObject
from pages import BASE_URL


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

    def view_course(self, course_id):
        """
        Go to the course with `course_id` (e.g. edx/Open_DemoX/edx_demo_course)
        """
        # This is currently implemented as a native link with some CSS styling
        # We retrieve the href and visit the link directly rather than
        # using Selenium click methods, since there isn't an easy
        # way to reference the links otherwise (no css id)
        links = [
            el['href'] for el in self.css_find('a.enter-course')
            if course_id in el['href']
        ]

        if len(links) > 1:
            msg = "Expected one link for course {0}, but found {1}.  Will use the first link.".format(course_id, len(links))
            self.warning(msg)
            self.browser.visit(links[0])

        elif len(links) < 1:
            msg = "No links found for course {0}".format(course_id)
            self.warning(msg)

        else:
            self.browser.visit(links[0])
