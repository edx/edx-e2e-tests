"""
Payment page.
"""
from __future__ import absolute_import

import six
from bok_choy.page_object import PageObject

from regression.pages.lms.constants import THIRD_PARTY_PAYMENTS_BASE_URL


class PaymentPage(PageObject):
    """
    Payment page
    """
    url = THIRD_PARTY_PAYMENTS_BASE_URL + 'checkout'

    def is_browser_on_page(self):
        return 'CyberSource' in self.q(css='#logo a').text

    def make_test_payment(self):
        """
        Fill payment on payment page with testing payment data
        """
        # Fill payment details
        fill_details = {
            '#bill_to_forename': 'first_name',
            '#bill_to_surname': 'last_name',
            '#bill_to_address_line1': 'address1',
            '#bill_to_address_line2': 'address2',
            '#bill_to_address_city': 'city',
            '#bill_to_address_postal_code': '23as23',
            '#bill_to_email': 'a@a.com',
            '#card_number': '4111111111111111',
            '#card_cvn': '937'
        }
        for css, value in six.iteritems(fill_details):
            self.q(css=css).fill(value)

        drop_downs = {
            'bill_to_address_country': 'BH',
            'card_expiry_month': '08',
            'card_expiry_year': '2020'
        }

        # Select drop downs
        for css, value in six.iteritems(drop_downs):
            self.q(
                css='select[name="{}"] option[value="{}"]'.format(css, value)
            ).click()

            self.wait_for(
                lambda: self.q(
                    css='select[name="{}"] option[value="{}"]'.format(
                        css, value)
                ).selected, "Correct value is selected"
            )

        # Click Visa type on Card Type radio button
        self.q(css='label[for=card_type_001]').filter(
            lambda elem: elem.text == 'Visa'
        ).click()

        # Click Pay button
        self.q(css='.right.complete.pay_button').click()
