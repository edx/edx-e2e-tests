"""
Unit tests for utils
"""
import unittest

from ddt import ddt, data, unpack

from regression.pages.common.utils import (
    get_target_url_from_text,
    get_enrollment_codes_from_email,
    remove_spaces_from_list_elements,
    extract_mmm_dd_yyyy_date_string_from_text,
    convert_date_format,
    extract_numerical_value_from_price_string,
    get_course_key_from_asset,
    get_course_number_from_course_id,
    substring_from
)
from regression.pages.common.tests.test_consts import (
    TARGET_URL_FROM_TEXT,
    REMOVE_SPACES_FROM_LIST,
    EXTRACT_MMM_DD_YYYY,
    CONVERT_DATE,
    EXTRACT_NUMERICAL_VALUE,
    FIND_SUBSTRING,
    COURSE_KEY_FROM_ASSET,
    COURSE_NUMBER_FROM_ID
)


@ddt
class TestUtils(unittest.TestCase):
    """
    Class for Utils unit tests
    """

    @data(
        TARGET_URL_FROM_TEXT['activation_link'],
        TARGET_URL_FROM_TEXT['password_reset_link'],
        TARGET_URL_FROM_TEXT['enrollment_codes_link'],
        TARGET_URL_FROM_TEXT['invalid_string'],
        TARGET_URL_FROM_TEXT['empty_text']
    )
    @unpack
    def test_get_target_url_from_text(
            self,
            partial_string,
            text_chunk,
            result
    ):
        """
        Test that regex is correctly extracting the target url based on
        partial string in different cases.
        Also test that in case the regex search is not successful a
        meaningful message is displayed
        Args:
            partial_string:
            text_chunk:
            result:
        """
        self.assertEqual(
            get_target_url_from_text(partial_string, text_chunk),
            result
        )

    @data()
    @unpack
    def test_get_enrollment_codes_from_email(self, source_data, result):
        self.assertEqual(
            get_enrollment_codes_from_email(source_data),
            result
        )

    @data(
        REMOVE_SPACES_FROM_LIST['list_without_spaces'],
        REMOVE_SPACES_FROM_LIST['list_with_spaces'],
        REMOVE_SPACES_FROM_LIST['empty_list']
    )
    @unpack
    def test_remove_spaces_from_list_elements(
            self,
            original_list,
            resulting_list
    ):
        """
        Test that spaces are removed from all elements of different types of
        lists
        Args:
            original_list:
            resulting_list:
        """
        self.assertEqual(
            remove_spaces_from_list_elements(original_list),
            resulting_list
        )

    @data(
        EXTRACT_MMM_DD_YYYY['course_start_date'],
        EXTRACT_MMM_DD_YYYY['discount_end_date'],
        EXTRACT_MMM_DD_YYYY['invalid_format']
    )
    @unpack
    def test_extract_mmm_dd_yyyy_date_string_from_text(
            self,
            original_string,
            result
    ):
        """
        Test that date of the format MMM dd, yyy can be extracted successfully
        from teh target string
        Also in case the date is not found a relevant error message is raised
        Args:
            original_string:
            result:
        """
        self.assertEqual(
            extract_mmm_dd_yyyy_date_string_from_text(original_string),
            result
        )

    @data(
        CONVERT_DATE['first'],
        CONVERT_DATE['second'],
        CONVERT_DATE['third'],
        CONVERT_DATE['fourth'],
        CONVERT_DATE['invalid_date'],
        CONVERT_DATE['invalid_format']
    )
    @unpack
    def test_convert_date_format(
            self,
            original_date,
            original_format,
            required_format,
            result
    ):
        """
        Test that dates can be changed from one format to other successfully
        Also in case of any error a relevant error message is displayed
        Args:
            original_date:
            original_format:
            required_format:
            result:

        Returns:

        """
        self.assertEqual(
            convert_date_format(
                original_date,
                original_format,
                required_format
            ),
            result
        )

    @data(
        EXTRACT_NUMERICAL_VALUE['normal_string_with_percentage_sign'],
        EXTRACT_NUMERICAL_VALUE['normal_string_with_dollar_sign'],
        EXTRACT_NUMERICAL_VALUE['string_with_comma'],
        EXTRACT_NUMERICAL_VALUE['string_with_decimal'],
        EXTRACT_NUMERICAL_VALUE['string_with_decimal_and_comma'],
        EXTRACT_NUMERICAL_VALUE['string_with_no_numbers']
    )
    @unpack
    def test_extract_numerical_value_from_price_string(
            self,
            price_strings,
            result
    ):
        """
        Test that regex is correctly extracting the numerical value from
        the string in different cases.
        Also test that in case the regex search is not successful a
        meaningful message is displayed
        Args:
            price_strings:
            result:
        """
        self.assertEqual(
            extract_numerical_value_from_price_string(price_strings),
            result
        )

    @data(
        FIND_SUBSTRING['asset_url'],
        FIND_SUBSTRING['normal_string'],
        FIND_SUBSTRING['invalid_delimiter']
    )
    @unpack
    def test_substring_from(
            self,
            original_string,
            target_delimiter,
            result
    ):
        """
        Test that correct substring is extracted in different cases
        Also test that in case the substring is not found a
        meaningful message is displayed
        Args:
            original_string:
            target_delimiter:
            result:
        """
        self.assertEqual(
            substring_from(original_string, target_delimiter),
            result
        )

    @data(
        COURSE_KEY_FROM_ASSET['mit_professionalx'],
        COURSE_KEY_FROM_ASSET['harvard_xplus'],
        COURSE_KEY_FROM_ASSET['harvard_mdeical_school']
    )
    @unpack
    def test_get_course_key_from_asset(
            self,
            opaque_asset,
            course_id
    ):
        """
        Test that edx opaque key extracts the course key from asset key
        Args:
            opaque_asset:
            course_id:
        """
        self.assertEqual(
            unicode(get_course_key_from_asset(opaque_asset)),
            course_id
        )

    @data(
        COURSE_NUMBER_FROM_ID['mit_professionalx'],
        COURSE_NUMBER_FROM_ID['harvard_xplus'],
        COURSE_NUMBER_FROM_ID['harvard_mdeical_school']
    )
    @unpack
    def test_get_course_number_from_course_id(
            self,
            course_id,
            course_number
    ):
        """
        Test that edx opaque key extracts the course key from asset key
        Args:
            course_id:
            course_number:
        """
        self.assertEqual(
            unicode(get_course_number_from_course_id(course_id)),
            course_number
        )
