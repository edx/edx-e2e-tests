from e2e_framework.page_object import PageObject
from selenium.common.exceptions import WebDriverException
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

    def course_id_list(self):
        """
        Retrieve the list of available course IDs
        on the page.
        """
        return [el['id'] for el in self.css_find('article.course')]

    def go_to_course(self, course_id):
        """
        Navigate to the course with `course_id`.
        Currently the course id has the form
        edx/999/2013_Spring, but this could change.
        """

        # Try clicking the link directly
        # There are several links without text;
        # in IE 10, only the second one works
        try:
            css = 'a[href="/courses/{0}/about"]'.format(course_id)
            self.css_click(css, index=1)

        # Chrome gives an error that another element would receive the click.
        # So click higher up in the DOM
        except WebDriverException:
            # We need to escape forward slashes in the course_id
            # to create a valid CSS selector
            course_id = course_id.replace('/', '\/')
            self.css_click('article.course#{0}'.format(course_id))
