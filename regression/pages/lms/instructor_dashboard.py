"""
Instructor dashboard page.
"""
from edxapp_acceptance.pages.lms.instructor_dashboard import (
    InstructorDashboardPage
)
from regression.pages.lms import BASE_URL


class InstructorDashboardPageExtended(InstructorDashboardPage):
    """
    This class is an extended class of Instructor Dashboard Page,
    where we add methods that are different or not used in
    InstructorDashboardPage
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return BASE_URL + "/courses/" + self.course_id + "/" + self.url_path

    def click_analytics_tab(self):
        """
        Clicks Analytics tab on Instructor Dashboard
        """
        self.q(css='[data-section="instructor_analytics"]').click()
        # Click initiates an ajax call
        self.wait_for_ajax()

    def click_edx_insights(self):
        """
        Clicks edX Insights link on Analytics tab
        """
        self.q(css='p em a').click()
        self.browser.switch_to_window(self.browser.window_handles[-1])
        return self.q(css='.navbar-brand-app').text[0]
