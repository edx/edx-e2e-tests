"""
Redeem coupon page
"""
from __future__ import absolute_import

import os

from bok_choy.page_object import PageObject
from opaque_keys.edx.keys import AssetKey

from regression.pages.common.utils import (
    convert_date_format,
    extract_mmm_dd_yyyy_date_string_from_text,
    extract_numerical_value_from_price_string
)
from regression.pages.whitelabel import ECOM_URL_WITH_AUTH


def get_course_ids_from_link(link):
    """
    Get course Ids from link.

    Arguments:
        link(str): The link to extract course id from.
    Returns:
        Course Ids
    """
    asset_str = link.partition('asset-v1')[1] + link.partition('asset-v1')[2]
    return AssetKey.from_string(asset_str).course_key


class RedeemCouponPage(PageObject):
    """
    Redeem Coupon page
    """

    def __init__(self, browser, coupon_code):
        """
        Enrollment code has to be set by the test
        """
        super(RedeemCouponPage, self).__init__(browser)
        self.coupon_code = coupon_code
        self.course_tile_css = 'div.discount-multiple-courses'

    @property
    def url(self):
        """
        Construct a URL to the page using the coupon code.
        """
        partial_url_string = 'coupons/offer/?code=' + self.coupon_code
        return os.path.join(ECOM_URL_WITH_AUTH, partial_url_string)

    def is_browser_on_page(self):
        return all(
            [self.q(css='.navbar-brand').present,
             self.q(css='.container').present]
        )

    def wait_for_course_tile(self):
        """
        Wait for course tiles to appear on page
        """
        self.wait_for_element_visibility(
            self.course_tile_css,
            'wait for course tile'
        )

    def get_course_info(self):
        """
        Get course info(name, org and start date).

        Returns:
            dict: A dictionary with keys for course name, org and start date.
        """
        return {
            'course_name': self.q(
                css='' + self.course_tile_css + ' .course-name'
            ).text[0],
            'course_org': self.q(
                css='' + self.course_tile_css + ' .course-org'
            ).text[0],
            'course_start_date': self.coupon_course_start_date
        }

    def click_checkout_button(self, course_id):
        """
        Click on Checkout button to go to basket page

        Arguments:
            course_id(str): id of the course.
        """
        self.q(
            css='#PurchaseCertificate[data-course-id="' + course_id + '"]'
        ).click()

    @property
    def coupon_course_start_date(self):
        """
        Get course start date

        Returns:
            str: Start data of course.
        """
        date_string = self.q(
            css='' + self.course_tile_css + ' .course-start'
        ).text[0]
        date_string = extract_mmm_dd_yyyy_date_string_from_text(date_string)
        # Convert date format to 0000-00-00T00:00:00
        return convert_date_format(
            date_string,
            '%b %d, %Y',
            '%Y-%m-%dT%H:%M:%S'
        )

    def get_course_discount_info(self):
        """
        Get course discount info

        Returns:
            dict: A dictionary with keys for course price, discount value,
                  benefit type and discounted price.
        """
        course_price_str = self.q(
            css=self.course_tile_css +
            ' .discount-mc-price-group .course-price>span'
        ).text[0]
        benefit_value_str = self.q(
            css=self.course_tile_css +
            ' .discount-percentage>p'
        ).text[0]
        discounted_price_str = self.q(
            css=self.course_tile_css +
            ' .discount-mc-price-group .course-new-price>span'
        ).text[0]
        return {
            'course_price': extract_numerical_value_from_price_string(
                course_price_str
            ),
            'benefit_value': extract_numerical_value_from_price_string(
                benefit_value_str
            ),
            'discounted_price': extract_numerical_value_from_price_string(
                discounted_price_str
            ),
            'benefit_type': self.benefit_type
        }

    @property
    def benefit_type(self):
        """
        Get benefit type

        Returns:
            str: Benefit type
        """
        discount_str = self.q(
            css='' + self.course_tile_css + ' .discount-percentage>p').text[0]
        if '$' in discount_str:
            return 'Absolute'
        return 'Percentage'

    @property
    def error_message(self):
        """
        Get the error message for invalid coupon

        Returns:
            str: The error message.
        """
        return self.q(css='.depth.depth-2.message-error-content>h3').text[0]

    def redeem_enrollment(self, target_page):
        """
        Click on Checkout button to go to basket page
        Args:
             target_page:
        """
        self.q(css=self.course_tile_css + ' #RedeemEnrollment').click()
        target_page.wait_for_page()

    def set_course_tile_index(self, course_title):
        """
        Get the course tile index place based on course title
        Args:
            course_title:
        """
        names = self.q(css='.discount-multiple-courses .course-name').text
        course_index = names.index(course_title)
        self.course_tile_css = self.course_tile_css + ":nth-child({})".format(
            course_index+2
        )


class RedeemCouponErrorPage(PageObject):
    """
    Redeem Coupon Error page
    """

    url = None

    def is_browser_on_page(self):
        return self.q(css='.depth.depth-2.message-error-content').present

    @property
    def error_message(self):
        """
        Get error message from the page
        Returns:
            error message:
        """
        return self.q(css='.depth.depth-2.message-error-content>h3').text[0]
