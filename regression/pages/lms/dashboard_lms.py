"""
Student dashboard page.
"""
from __future__ import absolute_import

from bok_choy.promise import BrokenPromise

from edxapp_acceptance.pages.lms.dashboard import DashboardPage
from regression.pages.lms import LOGIN_BASE_URL
from regression.pages.whitelabel.courses_page import CoursesPage


class DashboardPageExtended(DashboardPage):
    """
    This class is an extended class of Dashboard Page,
    where we add methods that are different or not used in DashboardPage
    """
    url = LOGIN_BASE_URL + '/dashboard'

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
        self.wait_for_element_visibility(
            '.action-donate', 'Donate button visibility'
        )
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

    def click_explore_courses_link(self):
        """
        Click Explore Courses link
        """
        self.q(css='.btn-neutral').click()
        courses_page = CoursesPage(self.browser)
        courses_page.wait_for_page()

    def is_secondary_account_message_visible(self, msg):
        """
        Is recovery Email account message visible?
        Returns:
            bool: True if secondary email message is visible:
        """
        return self.q(css='.msg .copy').filter(
            lambda elem: msg in elem.text
        ).visible
