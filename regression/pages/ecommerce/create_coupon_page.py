"""
Create coupon page
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import ECOMMERCE_URL_WITH_AUTH
from regression.pages.common.utils import (
    click_checkbox,
    fill_input_fields,
    select_value_from_drop_down
)
from regression.pages.ecommerce.created_coupon_page import CreatedCouponPage


class CreateCouponPage(PageObject):
    """
    Create Coupon Form
    """

    url = ECOMMERCE_URL_WITH_AUTH + 'coupons/' + 'new'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if coupons form is visible:
        """
        return self.q(css='.coupon-form-view').visible

    def fill_coupon_title(self, coupon_title):
        """
        Provide coupon title in create new coupon form
        Args:
             coupon_title:
        """
        self.q(css='input[name="title"]').fill(coupon_title)

    def fill_course_id(self, course_id):
        """
        Provide course id for single course coupon
        Args:
             course_id:
        """
        self.q(css='input[name="course_id"]').fill(course_id)
        self.wait_for_ajax()

    def verify_auto_population_of_seat_type(self, seat_type):
        """
        Verify that correct seat type is auto populated after course id
        is provided
        Args:
         seat_type:
        """
        self.wait_for(
            lambda: self.q(
                css='select[name="seat_type"] option[value="{}"]'.format(
                    seat_type
                )
            ).selected,
            "Correct seat type as per course is selected",
        )

    def fill_search_query(self, search_query):
        """
        Provide search criteria for multiple courses
        Args:
             search_query:
        """
        click_checkbox(self, '#multiple-courses')
        self.q(css='#catalog-query').fill(search_query)
        click_checkbox(self, '#professional')

    @property
    def multiple_courses_search_results(self):
        """
        Get multiple courses search results
        Returns:
            search results:
        """
        self.q(css='button[name="preview_catalog"]').click()
        self.wait_for_element_visibility(
            '#catalogModal>.modal-dialog',
            'Wait for Catalog dialog box'
        )
        self.wait_for_ajax()
        courses_list = self.q(
            css='#coursesTable>tbody>tr>td:nth-of-type(1)').text
        self.q(css='.modal-header>.close').click()
        self.wait_for_element_invisibility(
            '#catalogModal',
            'wait for catalog dialog box to close'
        )
        return courses_list

    def select_coupon_type(self, coupon_type):
        """
        Provide coupon code type in the create coupons form
        Args:
             coupon_type:
        """
        select_value_from_drop_down(self, "code_type", coupon_type)

    def select_category(self, category):
        """
        Provide coupon category in the create coupons form
        Args:
             category:
        """
        select_value_from_drop_down(self, "category", category)

    def set_dates(self, start_date, end_date):
        """
        Provide start date and end date for the coupon
        Args
            start_date:
            end_date:
        """
        fill_css_selectors = [
            'input[name="start_date"]',
            'input[name="end_date"]'
        ]
        fill_values = [start_date, end_date]
        fill_input_fields(self, fill_css_selectors, fill_values)

    def fill_email_domains(self, email_domains):
        """
        Provide comma separated email domains for restricting access
        Args:
         email_domains:
        """
        self.q(css='#email-domains').fill(email_domains)

    def select_voucher_type(self, voucher_type):
        """
        Select voucher usage type
        Args:
             voucher_type:
        """
        select_value_from_drop_down(self, "voucher_type", voucher_type)

    def fill_quantity(self, quantity):
        """
        Provide no of codes
        Args:
             quantity:
        """
        self.q(css='.form-control[name="quantity"]').fill(str(quantity))

    def max_uses(self, max_uses):
        """
        Provide maximum no of uses
        Args:
            max_uses:
        """
        self.q(css='.form-control[name="max_uses"]').fill(str(max_uses))

    def fill_coupon_benefit_value(self, benefit_value):
        """
        For discount coupons, provide discount value
        Args:
            benefit_value:
        """
        self.q(css='.form-control[name="benefit_value"]').fill(benefit_value)

    def select_benefit_type(self, benefit_type):
        """
        Select discount type
        Args:
            benefit_type:
        """
        if benefit_type == "Absolute":
            click_checkbox(self, '#benefit-fixed')
        else:
            click_checkbox(self, '#benefit-percent')

    def fill_coupon_client(self, client):
        """
        Provide client name
        Args:
             client:
        """
        self.q(css="input[name='client']").fill(client)

    def select_coupon_invoice_type(self):
        """
        Provide invoice type
        """
        click_checkbox(self, '.invoice-type>div>#not-applicable')

    def submit_coupon(self):
        """
        Click on the submit button to create the coupon based on provided
        information
        """
        self.q(css='button[type="submit"]').click()
        CreatedCouponPage(self.browser).wait_for_page()
