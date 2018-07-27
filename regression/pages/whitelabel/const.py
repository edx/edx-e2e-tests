# -*- coding: utf-8 -*-
"""
List of constants to be used throughout the tests
"""
import os

from regression.pages.whitelabel import (
    LMS_URL,
    ECOM_URL,
    ORG
)

# Global password
PASSWORD = os.environ.get('GLOBAL_PASSWORD')

# Client information for access token
SANDBOX_CLIENT_ID = "ecommerce-key"
OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID', SANDBOX_CLIENT_ID)
SANDBOX_CLIENT_SECRET = "ecommerce-secret"
OAUTH_CLIENT_SECRET = os.environ.get(
    'OAUTH_CLIENT_SECRET',
    SANDBOX_CLIENT_SECRET
)

# Organization Based Settings
##############################################################################

ECOMMERCE_API_URL = os.path.join(ECOM_URL, 'api/v2/')

ENROLLMENT_API_URL = os.path.join(LMS_URL, 'api/enrollment/v1')

CYBERSOURCE_CHECKOUT_URL = \
    u'https://testsecureacceptance.cybersource.com/checkout'

EMAIL_SENDER_ACCOUNTS = {
    'HarvardMedGlobalAcademy': 'support_cmeonline@hms.harvard.edu',
    'MITxPRO': 'mitxpro@mit.edu',
}

EMAIL_SENDER_ACCOUNT = EMAIL_SENDER_ACCOUNTS[ORG]

LOGO_LINKS = {
    'HarvardMedGlobalAcademy': 'hms-logo',
    'MITxPRO': 'mitx-pro-logo'
}

LOGO_LINK = LOGO_LINKS[ORG]

LOGO_ALT_TEXTS = {
    'HarvardMedGlobalAcademy': 'HMS Logo',
    'MITxPRO': 'MIT Logo'
}

LOGO_ALT_TEXT = LOGO_ALT_TEXTS[ORG]

SOCIAL_MEDIA_LINKS = {
    'HarvardMedGlobalAcademy': [
        'https://www.facebook.com/HarvardMed',
        'https://twitter.com/AcademyHms',
        'https://www.linkedin.com/company/harvard-medical-school-global-'
        'education',
        'https://instagram.com/harvardmed/?hl=en'
    ],
    'MITxPRO': []
}

SOCIAL_MEDIA_LINK = SOCIAL_MEDIA_LINKS[ORG]

##############################################################################

# REGISTRATION INFORMATION
REG_INFO = {
    'full_name': 'White label Test User',
    'first_name': 'White Label',
    'last_name': 'Test User',
    'gender': 'm',
    'yob': '1994',
    'state': 'Massachusetts',
    'country': 'US',
    'edu_level': 'm',
    'company': 'Arbisoft',
    'title': 'SQA'
}

# BILLING INFORMATION
CARD_HOLDER_INFO = {
    'first_name': 'billing',
    'last_name': 'user',
    'address01': '23-b',
    'address02': 'service lane',
    'city': 'Boston',
    'country': 'US',
    'state': 'MA',
    'postal_code': '02108',
    'email': 'billing_user@example.com'
}

# PAYMENT DETAILS
BILLING_INFO = {
    'card_type': 'visa',
    'card_number': '4111111111111111',
    'cvn': '123',
    'expiry_month': '07',
    'expiry_year': '2018'
}

# Existing user email
# EXISTING_USER_EMAIL = 'wl_smoke_user01@example.com'

# Staff user email
# STAFF_EMAIL = os.environ['STAFF_USER_EMAIL']

# Student user email
VISUAL_USER_EMAIL = 'wl_visual_test01@example.com'

# Default Threshold for visual difference
DIFF_THRESHOLD = 5000

# Timeouts
DEFAULT_TIMEOUT = 30

TIME_OUT_LIMIT = 90

SHORT_TIME_OUT_LIMIT = 30

INITIAL_WAIT_TIME = 3

WAIT_TIME = 5

# Countries and Languages Data

NO_OF_COUNTRIES = 250

NO_OF_LANGUAGES = 187

SAMPLE_COUNTRIES = [
    u'\xc5land Islands',
    u"C\xf4te d'Ivoire",
    u'Cura\xe7ao',
    u'Saint Helena, Ascension and Tristan da Cunha',
    u'Sint Maarten (Dutch part)'
]

SAMPLE_LANGUAGES = [
    u'Afrikaans',
    u'Sichuan Yi',
    u'Bokm\xe5l, Norwegian',
    u'Volap\xfck',
    u'Tonga (Tonga Islands)'
]

SELECTED_COUNTRY = u'United States of America'

SELECTED_LANGUAGE = u'English'

UNUSED_REGISTRATION_FIELDS_MAPPING = {
    "MITxPRO": ["profession", "specialty"],
    "HarvardMedGlobalAcademy": [
        'level_of_education',
        'gender',
        'company',
        'title',
        'honor_code'
    ]
}
