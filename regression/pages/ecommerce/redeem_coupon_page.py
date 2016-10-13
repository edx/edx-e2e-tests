"""
Redeem coupon page
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import ECOMMERCE_URL_WITH_AUTH
from regression.pages.common.utils import (
    extract_mmm_dd_yyyy_date_string_from_text,
    convert_date_format,
    extract_numerical_value_from_price_string,
    get_course_key_from_asset,
    substring_from
)


def get_course_ids_from_link(link):
    """
    Get course Ids from link
    Args:
        link:
    Returns:
        Course Ids
    """
    opaque_asset_key = substring_from(link, 'asset-v1')
    return get_course_key_from_asset(opaque_asset_key)


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
        self.course_tile = '.discount-multiple-courses>.box-shadow>div'

    @property
    def url(self):
        """
        Construct a URL to the page using the coupon code.
        """
        return (
            ECOMMERCE_URL_WITH_AUTH +
            'coupons/offer/?code=' +
            self.coupon_code
        )

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if offer is present:
        """
        return self.q(css='#offer').present

    def wait_for_course_tile(self):
        """
        Wait for course tiles to appear on page
        :return:
        """
        self.wait_for_element_visibility(
            self.course_tile, 'wait for course tile')

    @property
    def error_message(self):
        """
        Get the error message for invalid coupon
        Returns:
            error message:
        """
        return self.q(css='.depth.depth-2.message-error>h3').text[0]

    @property
    def course_info(self):
        """
        Get course info
        Returns:
            course name, org and course start date in a dictionary:
        """
        return {
            'course_name': self.q(
                css='' + self.course_tile + '>.course-name'
            ).text[0],
            'course_org': self.q(
                css='' + self.course_tile + '>.course-org'
            ).text[0],
            'course_start_date': self.course_start_date
        }

    @property
    def course_discount_info(self):
        """
        Get course discount info
        Returns:
            course price, discount value and discounted price in a
        dictionary:
        """
        course_price_str = self.q(
            css=self.course_tile +
            '>.discount-mc-price-group .course-price>span'
        ).text[0]
        benefit_value_str = self.q(
            css=self.course_tile +
            ' .discount-percentage>p'
        ).text[0]
        discounted_price_str = self.q(
            css=self.course_tile +
            '>.discount-mc-price-group .course-new-price>span'
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
            benefit type:
        """
        discount_str = self.q(
            css='' + self.course_tile + ' .discount-percentage>p').text[0]
        if '$' in discount_str:
            return 'Absolute'
        elif '%' in discount_str:
            return 'Percentage'

    @property
    def coupon_expiry_date(self):
        """
        Get coupon expiry date
        Returns:
            coupon expiry date:
        """
        date_string = self.q(
            css='' + self.course_tile + ' .voucher-valid-until>p'
        ).text[0]
        date_string = extract_mmm_dd_yyyy_date_string_from_text(date_string)
        # Convert date format to 0000-00-00T00:00:00
        return convert_date_format(
            date_string,
            '%b %d, %Y',
            '%Y-%m-%dT%H:%M:%S'
        )

    @property
    def course_start_date(self):
        """
        Get course start date
        Returns:
            course start date:
        """
        date_string = self.q(
            css='' + self.course_tile + '>.course-start'
        ).text[0]
        date_string = extract_mmm_dd_yyyy_date_string_from_text(date_string)
        # Convert date format to 0000-00-00T00:00:00
        return convert_date_format(
            date_string,
            '%b %d, %Y',
            '%Y-%m-%dT%H:%M:%S'
        )

    @property
    def course_image_text(self):
        """
        Get course image alt text from course tile
        Returns:
            alt text
        """
        return self.q(
            css='.discount-multiple-courses>.box-shadow img').attrs('alt')

    @property
    def course_ids_list(self):
        """
        Return the list of course ids
        Returns:
            Course Ids
        """
        image_links_list = self.q(
            css='.image-container>.img-responsive').attrs('src')
        ids_list = [
            get_course_ids_from_link(elem) for elem in image_links_list]
        return ids_list

    def checkout_discount_coupon(self, course_id, target_page):
        """
        Click on Checkout button to go to basket page
        Args:
            course_id:
            target_page:
        """
        self.q(
            css='#PurchaseCertificate[data-course-id="' + course_id + '"]'
        ).click()
        target_page.wait_for_page()

    def redeem_enrollment(self, target_page):
        """
        Click on Checkout button to go to basket page
        Args:
             target_page:
        """
        self.q(css='#RedeemEnrollment').click()
        target_page.wait_for_page()

    def display_error_message(self, course_id):
        """
        Click on Purchase certificate button to display error message
        Args:
            course_id:
        """
        self.q(
            css='#PurchaseCertificate[data-course-id="' + course_id + '"]'
        ).click()
        self.wait_for_ajax()
        self.wait_for_element_visibility(
            '.depth.depth-2.message-error', 'wait for error message')


class RedeemCouponErrorPage(PageObject):
    """
    Redeem Coupon Error page
    """

    url = None

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if error message is present:
        """
        return self.q(css='.depth.depth-2.message-error').present

    @property
    def error_message(self):
        """
        Get error message from the page
        Returns:
            error message:
        """
        return self.q(css='.depth.depth-2.message-error>h3').text[0]
