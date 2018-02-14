"""
Courses page
"""
from regression.tests.helpers.new_page_object import NewPageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH


class CoursesPage(NewPageObject):
    """
    Course Page
    """

    url = URL_WITH_AUTH + 'courses'

    def is_browser_on_page(self):
        return self.q(css='.course-name .course-title').visible

    def click_on_the_course(self, course_id):
        """
        click on the desired course id to open course about page

        Arguments:
            course_id(str): Id of the target page.
        """
        self.q(css='article[id="' + course_id + '"]>a').click()

    def go_to_course_about_page(self, target_page):
        """
        click on the desired course id to open course about page
        Args:
            target_page:
        """
        self.q(css='article[id="' + target_page.course_id + '"]>a').click()
        target_page.wait_for_page()
