"""
Dashboard page
"""
import re

from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH, DEFAULT_TIMEOUT
from regression.pages.whitelabel.course_info_page import CourseInfoPage
from regression.pages.whitelabel.courses_page import CoursesPage
from regression.pages.whitelabel.profile_page import ProfilePage


class DashboardPage(PageObject):
    """
    Dashboard page
    """

    url = URL_WITH_AUTH + u'dashboard'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if my courses header is visible:
        """
        return self.q(css='#my-courses').visible

    def is_course_present(self, course_id):
        """
        Verify that course is added to the dashboard
        Args:
         course_id:
        """
        course_number_search = re.search(r'(?<=\+)\w+(?=\+)', course_id)
        course_number = course_number_search.group(0)
        return self.q(
            css='#actions-dropdown-link-0[data-course-number="' +
            course_number + '"]'
        ).present

    def check_activation_message(self):
        """
        Verify that activation message is present on the dashboard
        """
        return self.q(css='.activation-message').present

    def unenroll_course(self, course_id):
        """
        Un-enroll the course
        Args:
             course_id:
        """
        course_number_search = re.search(r'(?<=\+)\w+(?=\+)', course_id)
        course_number = course_number_search.group(0)
        course_link = '#actions-dropdown-link-0[data-course-number="' + \
                      course_number + '"]'
        unenroll_item = '#actions-dropdown-list-0>#actions-item-unenroll-0>' \
                        '#unenroll-0'
        self.q(css=course_link).click()
        self.wait_for_element_visibility(
            unenroll_item,
            'unenroll option is visible',
            timeout=DEFAULT_TIMEOUT
        )
        self.q(css=unenroll_item).click()
        self.wait_for_element_visibility(
            '#unenroll-modal',
            'wait for popup',
            timeout=DEFAULT_TIMEOUT
        )
        self.q(css='.submit>input[value="Unenroll"]').click()
        self.wait_for_element_absence(
            course_link,
            'Course disappears from the dashboard',
            timeout=DEFAULT_TIMEOUT
        )

    def go_to_find_courses_page(self):
        """
        Click on the courses link to go to courses page
        """
        self.q(css='.brand-link[href="/courses"]').click()
        CoursesPage(self.browser).wait_for_page()

    def go_to_profile_page(self):
        """
        Select the My Profile page from profile drop down
        """
        self.q(css='.user-name').click()
        self.wait_for_element_visibility(
            '.show-user-menu',
            'wait for user dropdown to expand',
            timeout=DEFAULT_TIMEOUT
        )
        self.q(css='.show-user-menu>li>a[href^="/u/"]').click()
        ProfilePage(self.browser).wait_for_page()

    def go_to_course_info_page(self, course_id):
        """
        Click on the course link to go to course view page
        Args:
            course_id:
        """
        self.q(
            css='.course-title>a[href="/courses/' +
            course_id + '/info"]'
        ).click()
        CourseInfoPage(self.browser, course_id).wait_for_page()
