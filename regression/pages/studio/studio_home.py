"""
Dashboard page for Studio
"""
from edxapp_acceptance.pages.studio.index import DashboardPage
from bok_choy.promise import BrokenPromise
from regression.pages.studio import BASE_URL


class DashboardPageExtended(DashboardPage):
    """
    This class is an extended class of Studio Dashboard Page,
    where we add methods that are different or not used in DashboardPage
    """

    url = BASE_URL + '/home/'

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return self.q(css='.courses-tab.active').present

    def select_course(self, course_title):
        """
        Selects the course we want to perform tests on
        """
        course_names = self.q(css='.course-link h3')
        for vals in course_names:
            if course_title in vals.text:
                vals.click()
                return
        raise BrokenPromise('Course title not found')
