"""
Student dashboard page.
"""
from edxapp_acceptance.pages.lms.dashboard import DashboardPage
from bok_choy .promise import BrokenPromise
from regression.pages.lms import BASE_URL


class DashboardPageExtended(DashboardPage):
    """
    This class is an extended class of Dashboard Page,
    where we add methods that are different or not used in DashboardPage
    """
    url = BASE_URL + '/dashboard'

    def select_course(self, course_title):
        """
        Selects the course we want to perform tests on
        """
        course_names = self.q(css='.course-title a')
        for vals in course_names:
            if course_title in vals.text:
                vals.click()
                return
        raise BrokenPromise('Course title not found')

    def click_donate_button(self):
        """
        Clicks donate button on Dashboard
        """
        self.q(css='.action-donate').click()

    def logout_lms(self):
        """
        Clicks Drop down then SignOut button
        """
        self.q(css='.dropdown').click()
        self.wait_for_element_visibility(
            '.item a[href="/logout"]', 'SignOut button'
        )
        self.q(css='.item a[href="/logout"]').click()
