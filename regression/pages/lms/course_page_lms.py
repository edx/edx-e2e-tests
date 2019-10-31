"""
Course Home page
"""
from __future__ import absolute_import

from edxapp_acceptance.pages.lms.course_home import CourseHomePage
from regression.pages.lms import LOGIN_BASE_URL


class CourseHomePageExtended(CourseHomePage):
    """
    This class is an extended class of CourseHomePage,
    where we add methods that are different or not used in CourseHomePage
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, self.course_id, self.url_path
        )

    def click_resume_button(self):
        """
        Clicks Resume button of the course selected
        """
        self.q(css='.action-resume-course span').first.click()
