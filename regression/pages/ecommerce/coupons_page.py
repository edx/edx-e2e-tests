"""
Ecommerce coupons pages
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import (
    URL_WITH_AUTH,
    ECOMMERCE_URL_WITH_AUTH,
    ORG
)
from regression.pages.common.utils import fill_input_fields
from regression.pages.ecommerce.create_coupon_page import CreateCouponPage
from regression.pages.ecommerce.created_coupon_page import CreatedCouponPage


class Ecommerce(PageObject):
    """
    E-Commerce base class
    """

    url = URL_WITH_AUTH + 'login?next=/oauth2/authorize/confirm'

    def is_browser_on_page(self):
        """
        Verifies that login button is visible on the page
        """
        return self.q(
            css='.action.action-primary.action-update.js-login.login-button'
        ).visible


class EcommerceHome(PageObject):
    """
    E-Commerce Home
    """

    url = ECOMMERCE_URL_WITH_AUTH

    def is_browser_on_page(self):
        """
       Verifies that organization name is present in logo alt text:
        """
        return ORG.lower() in self.q(css='.navbar-brand-logo').attrs('alt')


class EcommerceCouponsHome(PageObject):
    """
    Logged out Coupons Page
    """

    url = ECOMMERCE_URL_WITH_AUTH + 'coupons'

    def is_browser_on_page(self):
        """
        Verifies that sign in button is visible:
        """
        return self.q(
            css='.action.action-primary.action-update.js-login.login-button'
        ).visible


class EcommerceLoginPage(PageObject):
    """
    E-Commerce Login Page
    """

    url = None

    def is_browser_on_page(self):
        """
        Verifies that login button is visible:
        """
        return self.q(
            css='.action.action-primary.action-update.js-login.login-button'
        ).visible

    def login_user_to_ecommerce(self, email, password):
        """
        Provide valid user credentials and login to ecommerce site
        Args:
            email:
            password:
        """
        elements_and_values = {
            '#login-email': email,
            '#login-password': password
        }
        fill_input_fields(self, elements_and_values)
        self.q(
            css='.action.action-primary.action-update.js-login.login-button'
        ).click()
        EcommerceCouponsPage(self.browser).wait_for_page()


class EcommerceCouponsPage(PageObject):
    """
    Logged in Coupons page
    """

    url = ECOMMERCE_URL_WITH_AUTH + 'coupons'

    def is_browser_on_page(self):
        """
        Verifies that coupons table is present
        """
        self.wait_for_ajax()
        return self.q(css='#couponTable').present

    def go_to_create_coupon_page(self):
        """
        Click on the create new coupon button
        """
        self.q(css='a[href="/coupons/new/"]').click()
        CreateCouponPage(self.browser).wait_for_page()

    def search_coupon(self, coupon_id):
        """
        Search Coupons
        Args:
            coupon_id:
        """
        search_input_box = '.field-input.input-text[ type="search"]'
        self.wait_for_element_visibility(
            search_input_box,
            'wait for search box'
        )
        self.q(css=search_input_box).fill(coupon_id)
        self.wait_for(
            lambda: self.q(
                css='#couponTable tr>td>a[class="coupon-title"]'
            ).filter(lambda el: el.text == coupon_id),
            'wait for search result'
        )

    def edit_coupon(self, coupon_id):
        """
        Edit Coupons
        Args:
            coupon_id:
        """
        self.q(
            css='#couponTable tr>td>a[class="coupon-title"]'
        ).filter(lambda el: el.text == coupon_id).click()
        CreatedCouponPage(self.browser).wait_for_page()
