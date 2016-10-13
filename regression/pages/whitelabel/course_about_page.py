"""
Course About page
"""
from bok_choy.page_object import PageObject

from regression.pages.ecommerce.basket_page import (
    SingleSeatBasketPage,
    MultiSeatBasketPage
)
from regression.pages.whitelabel.const import URL_WITH_AUTH
from regression.pages.whitelabel.inactive_account import InactiveAccount
from regression.pages.whitelabel.logistration_page import RegistrationPage


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
        Construct a URL to the page using the enrollment code.
        """
        return URL_WITH_AUTH + u"courses/" + self.course_id + u"/about"

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if enrollment button is present:
        """
        return self.q(css='.btn-enroll').present

    def is_course_already_on_cart(self):
        """
        Is course already present on cart?
        Returns:
            True if "course is in your cart message" is visible:
        """
        return 'This course is in your cart' in self.q(
            css='.btn-enroll'
        ).text[0]

    def is_enrollment_button_enabled(self):
        """
        Check if enrollment button is enabled
        Returns:
            True if button is enabled:
        """
        return self.q(
            css='.course-detail .btn-enroll'
        ).filter(lambda elem: elem.text == 'Enroll Now').present

    @property
    def add_to_cart_button_text(self):
        """
        get the text from add to cart button
        Returns:
            add to cart button text:
        """
        return self.q(css='.add-to-cart').text[0]

    @property
    def course_price(self):
        """
        Get and return course price from about page
        Returns:
            course price:
        """
        price = None
        if 'Price' in self.q(css='.col.col-12.sm-col-12.md-col-2').text[0]:
            price = self.q(css='.col.col-12.sm-col-12.md-col-2>span').text[0]
        return float(price[1:])

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
        RegistrationPage(self.browser).wait_for_page()

    def register_using_group_purchase_button(self):
        """
        Unregistered user clicks on the Bulk Purchase button to go to
        registration page
        """
        self.wait_for_element_visibility(
            '#ecommerce_bulk_checkout_button.register',
            'wait for registration button'
        )
        self.q(css='#ecommerce_bulk_checkout_button').click()
        RegistrationPage(self.browser).wait_for_page()

    def go_to_single_seat_basket_page(self):
        """
        Click on the Enroll button to go to single seat basket page
        """
        add_to_cart_button = '.course-detail .btn-enroll'
        self.wait_for_element_visibility(
            add_to_cart_button,
            'Enroll button is visible'
        )
        self.q(css=add_to_cart_button).click()
        SingleSeatBasketPage(self.browser).wait_for_page()

    def is_group_purchase_button_present(self):
        """
        Check if group purchase button is present
        """
        return self.q(css='#ecommerce_bulk_checkout_button').present

    def is_email_button_present(self):
        """
        Check if email us for group purchase button is present
        Returns:
            True if mailto: tag is present:
        """
        return self.q(css='.btn-enroll[href^="mailto:"]').present

    def go_to_multi_seat_basket_page(self):
        """
        Click on the Purchase for a group button to go to multi seat basket
        page
        """
        self.q(css='#ecommerce_bulk_checkout_button').click()
        MultiSeatBasketPage(self.browser).wait_for_page()

    def go_to_inactive_page(self):
        """
        Inactive user click on the Enroll Now button to go to Inactive message
        page
        """
        self.wait_for_element_visibility(
            '.course-detail .btn-enroll.register',
            'Enrollment button is visible'
        )
        self.q(css='.course-detail .btn-enroll').click()
        InactiveAccount(self.browser).wait_for_page()
