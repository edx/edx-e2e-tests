"""
Extended CoursePage.
"""
import abc

from edxapp_acceptance.pages.studio.course_page import CoursePage

from regression.pages.studio.utils import get_course_key
from regression.pages.studio import BASE_URL


class CoursePageExtended(CoursePage):
    """
    Extended CoursePage.
    """
    @abc.abstractmethod
    def is_browser_on_page(self):
        pass

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        course_key = get_course_key(self.course_info)
        return "/".join([BASE_URL, self.url_path, unicode(course_key)])
