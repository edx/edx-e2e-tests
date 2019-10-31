"""
Course About page
"""
from __future__ import absolute_import

import os

from bok_choy.page_object import PageObject

from regression.pages.whitelabel import LMS_URL_WITH_AUTH


class CourseAboutPage(PageObject):
    """
    Course About page class
    """

    def __init__(self, browser, course_id):
        """
        Course id has to be set by the test
        """
        super(CourseAboutPage, self).__init__(browser)
        self.course_id = course_id

    @property
    def url(self):
        """
        Construct url for the page.
        """
        partial_url_str = u"courses/" + self.course_id + u"/about"
        return os.path.join(LMS_URL_WITH_AUTH, partial_url_str)

    def is_browser_on_page(self):
        return all(
            [self.q(css='.btn-enroll').present,
             self.q(css='.hero-image').present]
        )

    @property
    def course_price(self):
        """
        Get and return course price from about page

        Returns:
            float: Price of course.
        """
        price = None
        if 'Price' in self.q(css='.col.col-12.sm-col-12.md-col-2').text[0]:
            price = self.q(css='.col.col-12.sm-col-12.md-col-2>span').text[0]
        return float(price[1:])

    def click_on_single_seat_basket(self):
        """
        Click on the Enroll button to go to single seat basket page
        """
        add_to_cart_button = '.course-detail .btn-enroll'
        self.wait_for_element_visibility(
            add_to_cart_button,
            'Enroll button is visible'
        )
        self.q(css=add_to_cart_button).click()

    def click_on_multi_seat_basket(self):
        """
        Click on the Purchase for a group button to go to multi seat basket
        page
        """
        multi_seat_basket_button_css = '#ecommerce_bulk_checkout_button'
        self.wait_for_element_visibility(
            multi_seat_basket_button_css,
            'Multi enroll button is visible.'
        )
        self.q(css=multi_seat_basket_button_css).click()

    def register_using_enrollment_button(self):
        """
        Unregistered user clicks on the Enroll Now button to go to registration
        page
        """
        self.wait_for_element_visibility(
            '.course-detail .btn-enroll.register',
            'Enrollment button is visible'
        )
        self.q(css='.course-detail .btn-enroll').click()
