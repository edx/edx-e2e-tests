from edxapp_pages.lms.course_info import CourseInfoPage


class CourseInfoPageExtended(CourseInfoPage):
    def click_resume_button(self):
        """
        Clicks Resume button of the course selected
        """
        self.q(css='.last-accessed-link').first.click()
