"""
Course Info Page
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH


class CourseInfoPage(PageObject):
    """
    Course Info Page Class
    """

    def __init__(self, browser, course_id):
        """
        Course id has to be set by the test
        """
        super(CourseInfoPage, self).__init__(browser)
        self.course_id = course_id

    @property
    def url(self):
        """
        Construct a URL to the page using the course id.
        """
        return URL_WITH_AUTH + u"courses/" + self.course_id + u"/info"

    def is_browser_on_page(self):
        return self.q(
            css='.active[href="/courses/' + self.course_id + '/info"]'
        ).present

    def is_staff_mode_on(self):
        """
        Is staff mode on?
        Returns:
            True if staff is selected in the view type:
        """
        return self.q(
            css='select[id="action-preview-select"] option[value="{}"]'.
            format('staff')
        ).selected
