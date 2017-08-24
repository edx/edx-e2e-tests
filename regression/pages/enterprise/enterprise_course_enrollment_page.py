"""
Enterprise Course Enrollment page
"""
from bok_choy.page_object import PageObject


class EnterpriseCourseEnrollment(PageObject):
    """
    Enterprise Course Enrollment class
    """

    url = None

    def is_browser_on_page(self):
        """
        Verifies if the Course confirmation title is visible on the page
        """
        return self.q(css='.course-confirmation-title').visible

    def get_course_title(self):
        """
        Returns course title
        """
        return self.q(css='.course-title').text[0]
