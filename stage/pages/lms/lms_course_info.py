from edxapp_pages.lms.course_info import CourseInfoPage
from . import BASE_URL


class LmsCourseInfoPage(CourseInfoPage):
    """
    Extended class of CourseInfoPage from lms/course_info
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return BASE_URL + "/courses/" + self.course_id + "/" + self.url_path

    def click_resume_button(self):
        """
        Clicks Resume button of the course selected
        """
        self.q(css='.last-accessed-link').first.click()
