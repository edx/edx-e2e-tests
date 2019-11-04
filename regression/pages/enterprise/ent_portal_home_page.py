"""
Enterprise portal login page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject


class EnterprisePortalHome(PageObject):
    """
    This class handles the IDP login page
    """
    url = None

    COURSE_LIST_CSS = '#__dialog2 #__dialog2-cont' \
                      ' #__xmlview0--todoList-listUl a'

    def wait_for_course_list(self):
        """
        Wait for course list to populate
        """
        self.wait_for(
            lambda:
            bool(self.q(css=self.COURSE_LIST_CSS).text),
            'wait for course list to populate'
        )

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return "Home" in self.q(css='#bizxSubTab_HOME_TAB').attrs('title')

    def open_courses_popup(self):
        """
        Open courses popup
        """
        self.wait_for_element_visibility('#__tile31', 'wait for courses box')
        self.q(css='#__tile31').click()
        self.wait_for_element_visibility('#__dialog2', 'wait for pop up')

    def fetch_course_titles_list(self):
        """
        Fetch course titles list
        Returns:
                Course titles list:
        """
        self.wait_for_course_list()
        return self.q(css=self.COURSE_LIST_CSS).text

    def open_enterprise_course_page(self, course_title_part):
        """
        Go to target enterprise course
        Arguments:
            course_title_part:
        """
        self.wait_for_course_list()
        self.q(
            css=self.COURSE_LIST_CSS
        ).filter(lambda ln: course_title_part in ln.text).click()
