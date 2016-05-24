from edxapp_pages.lms.dashboard import DashboardPage
from . import BASE_URL


class LmsDashboardPage(DashboardPage):
    """
    Extended class of DashboardPage from lms/dashboard
    """
    url = BASE_URL + '/dashboard'

    def select_course(self):
        """
        Selects the course we want to perform tests on
        Returns:
        """
        course_names = self.q(css='.course-title a')
        for vals in course_names:
            if 'Manual Smoke Test Course 1 - Auto' in vals.text:
                vals.click()
                break
