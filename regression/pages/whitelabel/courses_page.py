"""
Courses page
"""
from bok_choy.page_object import PageObject
from regression.pages.whitelabel.const import URL_WITH_AUTH


class CoursesPage(PageObject):
    """
    Course Page
    """

    url = URL_WITH_AUTH + 'courses'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if courses are visible on page:
        """
        return self.q(css='.course-name .course-title').visible

    def go_to_course_about_page(self, target_page):
        """
        click on the desired course id to open course about page
        Args:
            target_page:
        """
        self.q(css='article[id="' + target_page.course_id + '"]>a').click()
        target_page.wait_for_page()
