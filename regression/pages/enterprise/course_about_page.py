"""
Course about page
"""
from __future__ import absolute_import

import os

from bok_choy.page_object import PageObject

from regression.pages.enterprise.enterprise_const import ENT_COURSE_ID
from regression.pages.whitelabel import LMS_URL_WITH_AUTH


class CourseAboutPageExtended(PageObject):
    """
    Course about page
    """

    @property
    def url(self):
        """
        Construct url for the page.
        """
        partial_url_str = u"courses/" + ENT_COURSE_ID + u"/about"
        return os.path.join(LMS_URL_WITH_AUTH, partial_url_str)

    def is_browser_on_page(self):
        # Enroll in course button present on page
        return self.q(css='.register').present

    def get_course_title(self):
        """
        Returns course title
        """
        return self.q(css='.heading-group>h1').text[0]

    def click_enroll_button(self):
        """
        Click Enroll in a course button
        """
        self.q(css=".register").click()
