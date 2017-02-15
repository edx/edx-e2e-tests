"""
Voucher creation test helpers
"""
from regression.pages.ecommerce.coupons_page import (
    CreateCouponPage,
    CreatedCouponPage,
    Ecommerce,
    EcommerceCouponsHome,
    EcommerceLoginPage,
    EcommerceCouponsPage
)
from regression.pages.whitelabel.const import PASSWORD, STAFF_EMAIL


class VoucherCreation(object):
    """
    Class for creating Vouchers
    """

    def __init__(self, browser):
        """
        Initialize VoucherCreation objects
        """
        super(VoucherCreation, self).__init__()
        self.browser = browser
        # Initialize page objects
        self.create_coupon_page = CreateCouponPage(self.browser)
        self.created_coupon_page = CreatedCouponPage(self.browser)
        # Initialize coupon file
        self.coupon_file = ''

    def create_coupon(self, coupon):
        """
        Create coupons using the information sent by test
        Args:
            coupon:
        """
        self.visit_create_coupon_form()
        self.fill_coupon_form(coupon)
        self.submit_coupon_form()
        self.assert_created_coupon_details(coupon)

    def visit_create_coupon_form(self):
        """
        Login to ecommerce and open a create coupon form
        """
        Ecommerce(self.browser).visit()
        EcommerceCouponsHome(self.browser).visit()
        EcommerceLoginPage(self.browser).login_user_to_ecommerce(
            STAFF_EMAIL,
            PASSWORD
        )
        EcommerceCouponsPage(self.browser).go_to_create_coupon_page()

    def fill_coupon_form(self, coupon):
        """
        Fill form for the target coupon
        Args:
            coupon:
        """
        self.create_coupon_page.fill_coupon_title(coupon['title'])
        if coupon['catalog_type'] == 'Single course':
            self.create_coupon_page.fill_course_id(coupon['course_id'])
            self.create_coupon_page.verify_auto_population_of_seat_type(
                'Professional'
            )
        elif coupon['catalog_type'] == 'Multi course':
            self.create_coupon_page.fill_search_query(coupon['search_query'])
            # Make sure that search results are as expected
            assert sorted(coupon['search_results']) == sorted(
                self.create_coupon_page.get_multiple_courses_search_results())
        self.create_coupon_page.select_coupon_type(coupon['coupon_type'])
        self.create_coupon_page.set_dates(
            coupon['start_datetime'], coupon['end_datetime']
        )
        if 'email_domains' in coupon:
            self.create_coupon_page.fill_email_domains(coupon['email_domains'])
        self.create_coupon_page.select_voucher_type(coupon['voucher_type'])
        if 'quantity' in coupon:
            self.create_coupon_page.fill_quantity(coupon['quantity'])
        if 'max_uses' in coupon:
            self.create_coupon_page.fill_max_uses_field(coupon['max_uses'])
        if coupon['coupon_type'] == 'Discount code':
            self.create_coupon_page.fill_benefit_value(coupon['benefit_value'])
            self.create_coupon_page.select_benefit_type(coupon['benefit_type'])
        self.create_coupon_page.fill_coupon_client(coupon['client'])
        self.create_coupon_page.select_coupon_invoice_type()

    def submit_coupon_form(self):
        """
        submit form for the target coupon
        """
        self.create_coupon_page.submit_coupon()

    def assert_created_coupon_details(self, coupon):
        """
        Verify the details of created coupons
        Args:
            coupon:
        """
        if coupon['coupon_type'] == 'Enrollment code':
            assert self.created_coupon_page.coupon_type == \
                'Enrollment code', 'Coupon type is not correct'
        else:
            if coupon['benefit_type'] == 'Percentage' and \
                    coupon['benefit_value'] == 100:
                assert self.created_coupon_page.coupon_type == \
                    'Enrollment code', 'Coupon type is not correct'
            else:
                assert self.created_coupon_page.coupon_type == \
                    'Discount code', 'Coupon type is not correct'

    @property
    def coupon_id(self):
        """
        Get coupon Id from the download button link
        """
        return self.created_coupon_page.coupon_id
