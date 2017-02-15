"""
Created coupon page
"""
from bok_choy.page_object import PageObject


class CreatedCouponPage(PageObject):
    """
    Created Coupon page
    """

    url = None

    def is_browser_on_page(self):
        """
        Verifies that edit coupon button is visible:
        """
        return self.q(css='#CouponEdit').visible

    @property
    def coupon_type(self):
        """
        Get coupon type
        Returns:
            added coupon type:
        """
        return self.q(css='.coupon-type').text[0]

    @property
    def coupon_id(self):
        """
        Get id of coupon from download button
        Returns:
            coupons id:
        """
        coupon_id_link = self.q(
            css='.coupon-information .voucher-report-button'
        ).attrs('href')[0]
        coupon_id = coupon_id_link.split('/')
        return coupon_id[-2]
