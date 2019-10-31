"""
Student dashboard page.
"""
from __future__ import absolute_import

import os

from opaque_keys.edx.keys import CourseKey

from edxapp_acceptance.pages.lms.dashboard import DashboardPage
from regression.pages.whitelabel import LMS_URL_WITH_AUTH
from regression.pages.whitelabel.const import DEFAULT_TIMEOUT


class DashboardPageExtended(DashboardPage):
    """
    This class is an extended class of Dashboard Page,
    where we add methods that are different or not used in DashboardPage
    """
    url = os.path.join(LMS_URL_WITH_AUTH, u'dashboard')

    def logout_lms(self):
        """
        Log-out from LMS
        """
        log_out_button_css = '.user-account li>a[href="/logout"]'
        self.q(css='.user-name').click()
        self.wait_for_element_visibility(
            log_out_button_css,
            'wait for user dropdown to expand'
        )
        self.q(css=log_out_button_css).click()

    @property
    def is_activation_message_present(self):
        """
        Returns 'True' if account activation message is present on dashboard
        """
        return self.q(css='.activation-message').present

    def go_to_profile_page(self):
        """
        Select the My Profile page from profile drop down
        """
        self.q(css='.toggle-user-dropdown[aria-expanded="false"]').click()
        self.wait_for_element_visibility(
            '.toggle-user-dropdown[aria-expanded="true"]',
            'wait for user drop down to expand',
            timeout=DEFAULT_TIMEOUT
        )
        self.q(css='#user-menu a[href^="/u/"]').click()

    def is_course_present(self, course_id):
        """
        Checks whether course is present or not.

        Arguments:
            course_id(str): The unique course id.

        Returns:
            bool: True if the course is present.
        """
        course_number = CourseKey.from_string(course_id).course
        return self.q(
            css='#actions-dropdown-link-0[data-course-number="{}"]'.format(
                course_number
            )
        ).present

    def click_courses_button(self):
        """
        Click on the courses link to go to courses page
        """
        self.q(css='.nav-links a[href="/courses"]').click()

    def unenroll_course(self, course_id):
        """
        Un-enroll from the course

        Arguments:
             course_id(str): The unique id of the course to un-enroll from.
        """
        course_number = CourseKey.from_string(course_id).course
        course_link = '#actions-dropdown-link-0[data-course-number="' + \
                      course_number + '"]'
        un_enroll_button = '#actions-dropdown-list-0>#actions-item-unenroll' \
                           '-0>#unenroll-0'
        self.q(css=course_link).click()
        self.wait_for_element_visibility(
            un_enroll_button,
            'unenroll option is visible',
            timeout=DEFAULT_TIMEOUT
        )
        self.q(css=un_enroll_button).click()
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
