"""
Courseware page LMS
"""
from edxapp_acceptance.pages.lms.courseware import CoursewarePage
from regression.pages.lms import BASE_URL


class CoursewarePageExtended(CoursewarePage):
    """
    This class is an extended class of Courseware Page,
    where we add methods that are different or not used in
    Courseware Page
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return BASE_URL + "/courses/" + self.course_id + "/courseware"

    def view_unit_in_studio(self):
        """
        Clicks on the 'View unit in Studio' button
        """
        self.wait_for_element_visibility(
            '.instructor-info-action',
            'View unit in Studio link is visible'
        )
        self.q(css='.instructor-info-action').click()
