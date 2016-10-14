"""
Constants for Utils unit tests
"""

TARGET_URL_FROM_TEXT = {
    'activation_link': {
        'partial_string': 'activate',
        'text_chunk': """
        Thank you for creating an account with MIT Professional Education
        Digital Programs!

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
    'password_reset_link': {
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
    'enrollment_codes_link': {
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
    },
    'invalid_string': {
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
        """,
        'result':
            'Target URL not found in the text'
    },
    'empty_text': {
        'partial_string': 'activate',
        'text_chunk': """
        Some text without URL
        """,
        'result':
            'Target URL not found in the text'
    }
}

ENROLLMENT_CODES_FROM_EMAIL = {
    'valid_data': {
        'source_data': """
        Order Number:,MITPE-116375

        Enrollment code for professional seat in Internet of Things: Roadmap
        to a Connected World
        Code,Redemption URL
        AWMHEUSMXYZDJXRN,https://payments.mitprofessionalx-stage.mit.edu/
        coupons/offer/?code=AWMHEUSMXYZDJXRN
        PZBEQDSAVH26PPH4,https://payments.mitprofessionalx-stage.mit.edu/
        coupons/offer/?code=PZBEQDSAVH26PPH4
        DNMV2T6PJAUVZUHC,https://payments.mitprofessionalx-stage.mit.edu/
        coupons/offer/?code=DNMV2T6PJAUVZUHC
        """,
        'result': """
        AWMHEUSMXYZDJXRN,https://payments.mitprofessionalx-stage.mit.edu/
        coupons/offer/?code=AWMHEUSMXYZDJXRN
        PZBEQDSAVH26PPH4,https://payments.mitprofessionalx-stage.mit.edu/
        coupons/offer/?code=PZBEQDSAVH26PPH4
        DNMV2T6PJAUVZUHC,https://payments.mitprofessionalx-stage.mit.edu/
        coupons/offer/?code=DNMV2T6PJAUVZUHC
        """
    },
    'invalid_data': {
        'source_data': """
        Order Number:,MITPE-116375

        Enrollment code for professional seat in Internet of Things: Roadmap
        to a Connected World
        """,
        'result': "Coupons not found"
    }
}

REMOVE_SPACES_FROM_LIST = {
    'list_with_spaces': {
        "original_list": [
            'string with inner spaces',
            ' leftrightspaces ',
            ' outer and inner 12354 '
        ],
        "resulting_list": [
            'stringwithinnerspaces',
            'leftrightspaces',
            'outerandinner12354'
        ]
    },
    'list_without_spaces': {
        "original_list": [
            'nospaces',
            'charsand12354',
            ' ',
        ],
        "resulting_list": [
            'nospaces',
            'charsand12354',
            ''
        ]
    },
    'empty_list': {
        "original_list": [],
        "resulting_list": []
    }
}

EXTRACT_MMM_DD_YYYY = {
    'course_start_date': {
        'original_string': 'Course starts: May 04, 2016',
        'result': 'May 04, 2016'
    },
    'discount_end_date': {
        'original_string': 'Discount valid until Oct 31, 2016',
        'result': 'Oct 31, 2016'
    },
    'invalid_format': {
        'original_string': 'Discount valid until 31-OCT-1994',
        'result': 'Required date pattern not found in search string'
    }
}

CONVERT_DATE = {
    'first': {
        'original_date': 'Oct 31, 2016',
        'original_format': '%b %d, %Y',
        'required_format': '%Y-%m-%dT%H:%M:%S',
        'result': '2016-10-31T00:00:00'
    },
    'second': {
        'original_date': '2016-10-31T00:00:00',
        'original_format': '%Y-%m-%dT%H:%M:%S',
        'required_format': '%b %d, %Y',
        'result': 'Oct 31, 2016'
    },
    'third': {
        'original_date': '2013-1-25',
        'original_format': '%Y-%m-%d',
        'required_format': '%m/%d/%y',
        'result': '01/25/13'
    },
    'fourth': {
        'original_date': '15/2/2010',
        'original_format': '%d/%m/%Y',
        'required_format': '%a %b %d %Y',
        'result': 'Mon Feb 15 2010'
    },
    'fifth': {
        'original_date': '2016-10-13T22:09:36Z',
        'original_format': '%Y-%m-%dT%H:%M:%SZ',
        'required_format': '%Y-%m-%d',
        'result': '2016-10-14'
    },
    'invalid_date': {
        'original_date': 'ABC-1-25',
        'original_format': '%d/%m/%Y',
        'required_format': '%a %b %d %Y',
        'result': 'Invalid date or format'
    },
    'invalid_format': {
        'original_date': '2013-1-25',
        'original_format': 'abcdef',
        'required_format': '%a %b %d %Y',
        'result': 'Invalid date or format'
    }
}

EXTRACT_NUMERICAL_VALUE = {
    'normal_string_with_dollar_sign': {
        "price_strings": '$999',
        "result": 999
    },
    'normal_string_with_percentage_sign': {
        "price_strings": '99%',
        "result": 99
    },
    'string_with_comma': {
        "price_strings": '$999,99',
        "result": 99999
    },
    'string_with_decimal': {
        "price_strings": '55.90%',
        "result": 55.90
    },
    'string_with_decimal_and_comma': {
        "price_strings": '$999,99.99',
        "result": 99999.99
    },
    'string_with_no_numbers': {
        "price_strings": 'abcd',
        "result": 'No numerical value found in search string'
    }
}

FIND_SUBSTRING = {
    'asset_url': {
        'original_string': u'https://d3oqliy4hkdz86.cloudfront.net/asset-v1:'
                           u'MITProfessionalX+IOTx+2016_T1+type@asset+'
                           u'block@internet_of_thingscourse_card-v2-01.jpg',
        'target_delimiter': u'asset-v1',
        'result': u'asset-v1:MITProfessionalX+IOTx+2016_T1+type@asset+'
                  u'block@internet_of_thingscourse_card-v2-01.jpg'
    },
    'normal_string': {
        'original_string': u'This is a test string for substring from method',
        'target_delimiter': u'test',
        'result': u'test string for substring from method'
    },
    'invalid_delimiter': {
        'original_string': u'https://d3oqliy4hkdz86.cloudfront.net/asset-v1:'
                           u'MITProfessionalX+IOTx+2016_T1+type@asset+'
                           u'block@internet_of_thingscourse_card-v2-01.jpg',
        'target_delimiter': u'xxyyzz',
        'result': u'Target substring not found'
    }
}

COURSE_KEY_FROM_ASSET = {
    'mit_professionalx': {
        'opaque_asset': u'asset-v1:MITProfessionalX+IOTx+2016_T1+type@asset+'
                        u'block@internet_of_thingscourse_card-v2-01.jpg',
        'course_id': u'course-v1:MITProfessionalX+IOTx+2016_T1'
    },
    'harvard_xplus': {
        'opaque_asset': u'asset-v1:HarvardXPLUS+MCB63xPLUS+3T2016+type@asset+'
                        u'block@MCB63X_Thumbnail.png',
        'course_id': u'course-v1:HarvardXPLUS+MCB63xPLUS+3T2016'
    },
    'harvard_mdeical_school': {
        'opaque_asset': u'asset-v1:HarvardMedGlobalAcademy+KSCR+3T2016+type@'
                        u'asset+block@CR_v2.jpg',
        'course_id': u'course-v1:HarvardMedGlobalAcademy+KSCR+3T2016'
    }
}

COURSE_NUMBER_FROM_ID = {
    'mit_professionalx': {
        'course_id': u'course-v1:MITProfessionalX+IOTx+2016_T1',
        'course_number': u'IOTx'
    },
    'harvard_xplus': {
        'course_id': u'course-v1:HarvardXPLUS+MCB63xPLUS+3T2016',
        'course_number': u'MCB63xPLUS'
    },
    'harvard_mdeical_school': {
        'course_id': u'course-v1:HarvardMedGlobalAcademy+KSCR+3T2016',
        'course_number': u'KSCR'
    }
}
