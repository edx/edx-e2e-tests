from bok_choy.page_object import PageObject
from bok_choy.promise import EmptyPromise, fulfill_after
from ..lms import BASE_URL


class CourseAboutPage(PageObject):
    """
    Course about page (with registration button)
    """

    @property
    def name(self):
        return "lms.course_about"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self, course_id=None):
        """
        URL for the about page of a course.
        Course ID is currently of the form "edx/999/2013_Spring"
        but this format could change.
        """
        if course_id is None:
            raise NotImplemented("Must provide a course ID to access about page")

        return BASE_URL + "/courses/" + course_id + "about"

    def is_browser_on_page(self):
        return self.is_css_present('section.course-info')

    def register(self):
        """
        Register for the course on the page.
        """
        next_page_promise = EmptyPromise(
            lambda: "register" in self.browser.url,
            "on the registration page"
        )

        with fulfill_after(next_page_promise):
            self.css_click('a.register')
