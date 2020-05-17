"""
Coupon(voucher) class.
"""
from __future__ import absolute_import

import uuid

from regression.tests.helpers.api_clients import EcommerceApiClient
from regression.tests.helpers.coupon_consts import (
    BENEFIT_TYPE, COUPON_TYPE,
    DEFAULT_END_DATE,
    DEFAULT_START_DATE
)


class Coupon:
    """
    All common functions and attributes related to coupons.
    """
    def __init__(self, catalog_type, coupon_type, voucher_type, **kwargs):
        super(Coupon, self).__init__()
        self.benefit_type = ""
        self.benefit_value = ""
        self.discounted_course_price = ""
        self.coupon_id = ""
        self.e_commerce_api = EcommerceApiClient()
        self.coupon_data = self._set_coupon_data(
            catalog_type, coupon_type, voucher_type
        )
        if kwargs:
            self.coupon_data.update(kwargs)

    def _set_coupon_data(
            self,
            catalog_type,
            coupon_type,
            voucher_type,
    ):
        """
        Return all data needed to configure a coupon.

        There are two coupon types, and three subtypes of each coupon.

        Arguments:
            catalog_type(str): The type of catalog.
            coupon_type(str): The type of coupon i.e. single or multiple.
            voucher_type(str): Subtype of coupon i.e. Single use, multi-use,
                               or Once per customer

        Returns:
            dict: A dictionary with all data.
        """
        coupon_data = {
            "id": "null",
            "title": str(uuid.uuid4().node),
            "catalog_type": catalog_type,
            "code": "",
            "price": "0",
            "quantity": 1,
            "seats": [],
            "course_seats": [],
            "coupon_type": coupon_type,
            "voucher_type": voucher_type,
            "benefit_type": BENEFIT_TYPE['per'],
            "benefit_value": 100,
            "category": {"id": 3, "name": "Affiliate Promotion"},
            "start_datetime": DEFAULT_START_DATE,
            "end_datetime": DEFAULT_END_DATE,
            "client": "Test Client",
            "invoice_type": "Not-Applicable"
        }
        return coupon_data

    def set_discount_details(self):
        """
        Set discount value and type to be used in different calculations.

        By default the discount value and type are set to denote an enrollment
        coupon
        """
        self.benefit_value = 100
        self.benefit_type = BENEFIT_TYPE['per']
        if self.coupon_data['coupon_type'] == COUPON_TYPE['disc']:
            self.benefit_type = self.coupon_data['benefit_type']
            self.benefit_value = self.coupon_data['benefit_value']

    def set_discounted_course_price(self, course_price):
        """
        Calculate discount price for a course after applying coupon.

        Perform calculation for discounted amount for Absolute discount

        Arguments:
            course_price(float): The original course price.
        """
        if self.benefit_type == BENEFIT_TYPE['abs']:
            self.discounted_course_price = (
                course_price - float(self.benefit_value)
            )
        else:
            self.discounted_course_price = course_price - \
                (course_price * float(self.benefit_value)) / 100

    def setup_coupons_using_api(self, course_price):
        """
        Create and apply coupon on course using e-commerce api.

        Arguments:
            course_price(float): The original course price.
        """
        self.coupon_id = self.e_commerce_api.create_coupon(self.coupon_data)
        self.set_discount_details()
        self.set_discounted_course_price(course_price)

    @property
    def coupon_codes(self):
        """
        Get coupon codes from coupon report

        Returns:
            list: A list of coupon codes.
        """
        return self.e_commerce_api.get_coupon_codes(self.coupon_id)

    def delete_coupon(self):
        """
        Deletes coupon using e-commerce api.
        """
        self.e_commerce_api.delete_coupon(self.coupon_id)
