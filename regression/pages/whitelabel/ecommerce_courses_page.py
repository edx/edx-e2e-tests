"""
Logout Page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.lms import ECOM_BASE_URL


class EcommerceCoursesPage(PageObject):
    """
    E-Commerce Courses Page
    """

    url = ECOM_BASE_URL + '/courses'

    def is_browser_on_page(self):
        return self.q(css='.login-button').visible
