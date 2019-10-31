# -*- coding: utf-8 -*-

"""
Different utilities to be used in tests
"""
from __future__ import absolute_import

import datetime
import re

import six


def get_target_url_from_text(url_matching_string, text_chunk):
    """
    Search and return the target url from text chunk, the url is searched
    on the basis of partial string embedded in url
    Args:
        url_matching_string:
        text_chunk:
    Returns:
        target url:
    """
    pattern = r"(?P<url>http[s]?://[^\s]+(/{}/)[^\s]+)".format(
        url_matching_string
    )
    regex_result = re.search(pattern, text_chunk)
    if regex_result:
        target_url = regex_result.group("url")
        return target_url.rstrip('.')
    return 'Target URL not found in the text'


def read_enrollment_codes_from_text(coupon_string):
    """
    Read enrollment codes and urls from email
    Args:
        coupon_string:
    Returns:
        coupon codes and urls:
    """
    coupons = {}
    for row in coupon_string.splitlines():
        # Read the coupons starting from line 5
        new_row = row.split(',')
        # Check that first cell in row is a coupon code by checking it's
        # length, type and capitalization
        if len(new_row[0]) == 16 and \
                new_row[0].isalnum() and \
                new_row[0].isupper():
            coupons.update({new_row[0]: new_row[1]})
    if coupons:
        return coupons
    return 'Coupons not found'


def fill_input_fields(page, selectors_and_values_dict):
    """
    A helper function to fill multiple fields in a form
    Args:
        page:
        selectors_and_values_dict:
    """
    for key, value in six.iteritems(selectors_and_values_dict):
        page.q(css=key).fill(value)


def select_value_from_drop_down(page, drop_down_name, value):
    """
    A helper function to select value from drop down
    Args:
        page:
        drop_down_name:
        value:
    """
    page.wait_for_element_visibility(
        'select[name={}]'.format(drop_down_name), 'Drop down is visible')
    page.q(
        css='select[name={}] option[value="{}"]'.format(drop_down_name, value)
    ).click()
    page.wait_for(
        lambda: page.q(
            css='select[name={}] option[value="{}"]'.
            format(drop_down_name, value)
        ).selected, "Correct value is selected"
    )


def click_checkbox(page, css_selector):
    """
    A helper function to click check boxes
    Args:
       page:
       css_selector:
    """
    # pylint: disable=unnecessary-lambda
    page.wait_for_element_visibility(css_selector, 'wait for target checkbox')
    page_elem = page.q(css=css_selector).results[0]
    page.wait_for(
        lambda: not page_elem.is_selected(),
        'Target checkbox is not selected'
        )
    page.browser.execute_script("arguments[0].click();", page_elem)
    page.wait_for(
        lambda: page_elem.is_selected(),
        'Target checkbox is selected'
    )


def get_text_from_page_elements(page, elements):
    """
    A helper function to get text values for a dict of web elements
    Args:
        page:
        elements:
    Returns:
        text dict:
    """
    results = {}
    for key, value in six.iteritems(elements):
        results[key] = page.q(css=value).text[0]
    return results


def extract_mmm_dd_yyyy_date_string_from_text(text_string):
    """
    Extract date of MM dd, yyyy from text chunk
    Args:
        text_string:
    Returns:
        date
    """
    regex_result = re.search(
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}',
        text_string
    )
    if regex_result:
        date_string = regex_result.group(0)
        return date_string
    return 'Required date pattern not found in search string'


def convert_date_format(original_date, original_format, required_format):
    """
    Convert dates format to required pattern
    Args:
       original_date:
       original_format:
       required_format:
    Returns:
       modified date:
    """
    try:
        return datetime.datetime.strptime(
            original_date,
            original_format
        ).strftime(required_format)
    except ValueError:
        return 'Invalid date or format'


def extract_numerical_value_from_price_string(raw_price_string):
    """
    Extract numerical value from a string containing price
    Args:
        raw_price_string:
    Returns:
        numerical price:
    """
    regex_result = re.search(
        r'\d+,\d+\.\d+|\d+\.\d+|\.\d+|\d+,\d+|\d+',
        raw_price_string
    )
    if regex_result is not None:
        price_value = regex_result.group(0)
        return float(price_value.replace(",", ""))
    return 'No numerical value found in search string'


def extract_discount_value_from_response(catalog_uuid, offers_response):
    """
    Extract numerical value from a string containing price
    Args:
        catalog_uuid:
        offers_response:
    Returns:
        numerical price:
    """
    regex = r'.+Percentage.+?(\d+,\d+\.\d+|\d+\.\d+|\.\d+|\d+,\d+|\d+)'
    offer_value = re.findall(
        catalog_uuid + regex, offers_response, flags=re.DOTALL
    )
    if offer_value:
        return float(offer_value[0].replace(",", ""))
    return 'No Numerical value found in search string'
