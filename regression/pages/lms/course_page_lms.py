from edxapp_pages.lms.course_info import CourseInfoPage


class CourseInfoPageExtended(CourseInfoPage):
    """
    This class is an extended class of CourseInfoPage,
    where we add methods that are different or not used in CourseInfoPage
    """
    def click_resume_button(self):
        """
        Clicks Resume button of the course selected
        """
        self.q(css='.last-accessed-link').first.click()
