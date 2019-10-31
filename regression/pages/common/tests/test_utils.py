"""
Unit tests for utils
"""
from __future__ import absolute_import

import textwrap
import unittest

from ddt import data, ddt, unpack

from regression.pages.common.utils import (
    convert_date_format,
    extract_mmm_dd_yyyy_date_string_from_text,
    extract_numerical_value_from_price_string,
    get_target_url_from_text,
    read_enrollment_codes_from_text
)


@ddt
class TestUtils(unittest.TestCase):
    """
    Class for Utils unit tests
    """

    @data(
        {
            'partial_string': 'activate',
            'text_chunk': """
            Thank you for creating an account with our site.

            There's just one more step before you can enroll in a course: you
            need to activate your example organization account.
            To activate your account, click the following link. If that
            doesn't work, copy and paste the link into your browser's
            address bar.

            https://example-site.edu/activate/f290d7a1745a4839b8.
            If you didn't create an account, you don't need to do anything;
            you won't receive any more email from us. If you need assistance,
            please do not reply to this email message. Check the help section
            of the Organization website
            """,
            'result':
                'https://example-site.edu/activate/f290d7a1745a4839b8'
        },
        {
            'partial_string': 'password_reset_confirm',
            'text_chunk': """
            You're receiving this e-mail because you requested a password
            reset for your user account at example.edu.

            Please go to the following page and choose a new password:

            https://example-site.edu/password_reset_confirm/336nr-4/


            If you didn't request this change, you can disregard this email -
            we have not yet reset your password.

            Thanks for using our site!

            The Example Organization Team
            """,
            'result':
                'https://example-site.edu/password_reset_confirm/336nr-4/'
        },
        {
            'partial_string': 'enrollment_code_csv',
            'text_chunk': """
            Order confirmation for: EXM-123

            Dear User,

            Thank you for purchasing access to Example Course. Please go to
            https://example-site.edu/coupons/enrollment_code_csv/EXM-123/
            to download a CSV file with the enrollment codes for this course.
            Once you have the codes you can distribute them to your team.

            To explore other courses,
            please visit https://example-site.edu.

            Thank you,
            Example Organization Team

            You received this message because you purchased enrollment codes
            for Example course on https://example.edu.
            If you have any questions, please visit
            https://example-site.edu/contact.
            """,
            'result':
                'https://example-site.edu/coupons/enrollment_code_csv/EXM-123/'
        }
    )
    @unpack
    def test_get_target_url_from_text_with_valid_data(
            self,
            partial_string,
            text_chunk,
            result
    ):
        """
        Test that regex is correctly extracting the target url based on
        partial string in different cases.
        Args:
            partial_string:
            text_chunk:
            result:
        """
        self.assertEqual(
            get_target_url_from_text(partial_string, text_chunk),
            result
        )

    @data(
        {
            'partial_string': 'invalid_string',
            'text_chunk': """
            Order confirmation for: EXM-123

            Dear User,

            Thank you for purchasing access to Example Course. Please go to
            https://example-site.edu/coupons/enrollment_code_csv/EXM-123/
            to download a CSV file with the enrollment codes for this course.
            Once you have the codes you can distribute them to your team.

            To explore other courses,
            please visit https://example-site.edu.

            Thank you,
            Example Organization Team

            You received this message because you purchased enrollment codes
            for Example course on https://example.edu.
            If you have any questions, please visit
            https://example-site.edu/contact.
            """
        },
        {
            'partial_string': 'activate',
            'text_chunk': """
            Some text without URL
            """
        }
    )
    @unpack
    def test_get_target_url_from_text_with_invalid_data(
            self,
            partial_string,
            text_chunk
    ):
        """
        Test that in case the regex search is not successful a
        meaningful message is displayed
        Args:
            partial_string:
            text_chunk:
        """
        self.assertEqual(
            get_target_url_from_text(partial_string, text_chunk),
            'Target URL not found in the text'
        )

    @data(
        {
            'source_data': textwrap.dedent("""\
            Order Number:,EXAMPLE-116375

            Enrollment code for professional seat in course
            Code,Redemption URL
            AWMHEUSMXYZDJXRN,https://coupons/?code=AWMHEUSMXYZDJXRN
            PZBEQDSAVH26PPH4,https://coupons/?code=PZBEQDSAVH26PPH4
            DNMV2T6PJAUVZUHC,https://coupons/?code=DNMV2T6PJAUVZUHC"""),
            'result':
            {
                'AWMHEUSMXYZDJXRN': 'https://coupons/?code=AWMHEUSMXYZDJXRN',
                'PZBEQDSAVH26PPH4': 'https://coupons/?code=PZBEQDSAVH26PPH4',
                'DNMV2T6PJAUVZUHC': 'https://coupons/?code=DNMV2T6PJAUVZUHC'
            },
        },
        {
            'source_data': textwrap.dedent("""\
            Order Number:,EXAMPLE-116375

            Enrollment code for professional seat in course
            Code,Redemption URL
            AWMHEUSMXYZDJXRN,https://coupons/?code=AWMHEUSMXYZDJXRN
            PZBEQDSAVH26PPH4,https://coupons/?code=PZBEQDSAVH26PPH4
            DNMV2T6PJAUVZUHC,https://coupons/?code=DNMV2T6PJAUVZUHC"""),
            'result':
            {
                'AWMHEUSMXYZDJXRN': 'https://coupons/?code=AWMHEUSMXYZDJXRN',
                'PZBEQDSAVH26PPH4': 'https://coupons/?code=PZBEQDSAVH26PPH4',
                'DNMV2T6PJAUVZUHC': 'https://coupons/?code=DNMV2T6PJAUVZUHC'
            }
        }
    )
    @unpack
    def test_get_enrollment_codes_from_email_with_valid_data(
            self,
            source_data,
            result
    ):
        """
        Test that coupon codes are read successfully from email
        Args:
            source_data:
            result:
        """
        self.assertDictEqual(
            read_enrollment_codes_from_text(source_data),
            result
        )

    @data(
        """
        Order Number:,MITPE-116375

        Enrollment code for invalid course
        """,
        textwrap.dedent("""\
        Order Number:,MITPE-116375

        Enrollment code for invalid course
        abc123,https://coupons/?code=abc
        yth765,https://coupons/?code=thtg
        """)
    )
    def test_get_enrollment_codes_from_email_with_invalid_data(
            self,
            source_data
    ):
        """
        Test that a relevant error message is displayed when coupons are not
        found
        Args:
            source_data:
        """
        self.assertEqual(
            read_enrollment_codes_from_text(source_data),
            'Coupons not found'
        )

    @data(
        {
            'original_string': 'Course starts: May 04, 2016',
            'result': 'May 04, 2016'
        },
        {
            'original_string': 'Discount valid until Oct 31, 2016',
            'result': 'Oct 31, 2016'
        }
    )
    @unpack
    def test_extract_mmm_dd_yyyy_date_string_from_text_with_valid_data(
            self,
            original_string,
            result
    ):
        """
        Test that date of the format MMM dd, yyy can be extracted successfully
        from teh target string
        Args:
            original_string:
            result:
        """
        self.assertEqual(
            extract_mmm_dd_yyyy_date_string_from_text(original_string),
            result
        )

    @data('Course Start: 07-12-15', 'No date')
    def test_extract_mmm_dd_yyyy_date_string_from_text_with_invalid_data(
            self,
            original_string
    ):
        """
        Test in case the date is not found a relevant error message is raised
        Args:
            original_string:
        """
        self.assertEqual(
            extract_mmm_dd_yyyy_date_string_from_text(original_string),
            'Required date pattern not found in search string'
        )

    @data(
        {
            'original_date': 'Oct 31, 2016',
            'original_format': '%b %d, %Y',
            'required_format': '%Y-%m-%dT%H:%M:%S',
            'result': '2016-10-31T00:00:00'
        },
        {
            'original_date': '2016-10-31T00:00:00',
            'original_format': '%Y-%m-%dT%H:%M:%S',
            'required_format': '%b %d, %Y',
            'result': 'Oct 31, 2016'
        },
        {
            'original_date': '2013-1-25',
            'original_format': '%Y-%m-%d',
            'required_format': '%m/%d/%y',
            'result': '01/25/13'
        },
        {
            'original_date': '15/2/2010',
            'original_format': '%d/%m/%Y',
            'required_format': '%a %b %d %Y',
            'result': 'Mon Feb 15 2010'
        },
        {
            'original_date': '2016-10-13T22:09:36Z',
            'original_format': '%Y-%m-%dT%H:%M:%SZ',
            'required_format': '%Y-%m-%d',
            'result': '2016-10-13'
        }
    )
    @unpack
    def test_convert_date_format_with_valid_data(
            self,
            original_date,
            original_format,
            required_format,
            result
    ):
        """
        Test that dates can be changed from one format to other successfully
        Args:
            original_date:
            original_format:
            required_format:
            result:
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
        {
            'original_date': 'ABC-1-25',
            'original_format': '%d/%m/%Y',
            'required_format': '%a %b %d %Y',
        },
        {
            'original_date': '2013-1-25',
            'original_format': 'abcdef',
            'required_format': '%a %b %d %Y',
        }
    )
    @unpack
    def test_convert_date_format_with_invalid_data(
            self,
            original_date,
            original_format,
            required_format
    ):
        """
        Test that in case of any error a relevant error message is displayed
        Args:
            original_date:
            original_format:
            required_format:
        """
        self.assertEqual(
            convert_date_format(
                original_date,
                original_format,
                required_format
            ),
            'Invalid date or format'
        )

    @data(
        {
            "price_strings": '$999',
            "result": 999
        },
        {
            "price_strings": '99%',
            "result": 99
        },
        {
            "price_strings": '$999,99',
            "result": 99999
        },
        {
            "price_strings": '0(USD)',
            "result": 0
        },
        {
            "price_strings": '$999,99',
            "result": 99999
        }
    )
    @unpack
    def test_extract_numerical_value_from_price_string_with_integers(
            self,
            price_strings,
            result
    ):
        """
        Test that regex is correctly extracting the integral value from
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
        {
            "price_strings": '$999.99',
            "result": 999.99
        },
        {
            "price_strings": '9.9%',
            "result": 9.9
        },
        {
            "price_strings": '$.999',
            "result": .999
        },
        {
            "price_strings": '55.90%',
            "result": 55.90
        },
        {
            "price_strings": '$999,99.99',
            "result": 99999.99
        }
    )
    @unpack
    def test_extract_numerical_value_from_price_string_with_floats(
            self,
            price_strings,
            result
    ):
        """
        Test that regex is correctly extracting the floating point value from
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

    @data('abcd', '#$#$*')
    def test_extract_numerical_value_from_price_string_invalid(
            self,
            value
    ):
        """
        Test that in case the regex search is not successful a
        meaningful message is displayed
        Args:
            value:
        """
        self.assertEqual(
            extract_numerical_value_from_price_string(value),
            'No numerical value found in search string'
        )
