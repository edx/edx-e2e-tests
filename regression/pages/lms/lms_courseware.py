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
        self.q(css='.instructor-info-action').click()

    def get_page_names_in_tab(self):
        """
        Get names of all pages in tab

        Returns
            list: A list of names of all pages
        """
        tab_pages = self.q(css='.tabs.course-tabs .tab').text
        # There is an extra text 'Current location' along
        # the page's name of selected(active) tab. It is
        # not required, so removing it.
        return [page.replace('\n, current location', "") for page in tab_pages]
