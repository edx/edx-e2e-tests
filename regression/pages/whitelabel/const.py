# -*- coding: utf-8 -*-
"""
List of constants to be used throughout the tests
"""
import os

# Get HTTP Authentication credentials from environment variables
AUTH_USERNAME = os.environ['BASIC_AUTH_USER']
AUTH_PASSWORD = os.environ['BASIC_AUTH_PASSWORD']

# Get API Access token

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

# Select the Org for which to run the tests, Default is MITProfessionalX
ORG = os.getenv('ORG', 'MITProfessionalX')

# TEST EMAIL account
TEST_EMAIL_SERVICE = os.environ['TEST_EMAIL_SERVICE']
TEST_EMAIL_ACCOUNT = os.environ['TEST_EMAIL_ACCOUNT']
DEFAULT_TEST_EMAIL_ACCOUNT = TEST_EMAIL_ACCOUNT.format("")
TEST_EMAIL_PASSWORD = os.environ['TEST_EMAIL_PASSWORD']

# Global password
PASSWORD = os.environ['GLOBAL_PASSWORD']

BASIC_AUTH = AUTH_USERNAME + ":" + AUTH_PASSWORD + "@"

# Organization Based Settings
##############################################################################
# E-commerce raw url
RAW_ECOMMERCE_URL = {
    'HarvardMedGlobalAcademy':
        u'https://{}payments.globalacademy-stage.hms.harvard.edu/',
    'HarvardXPLUS': u'https://{}stage-payments.harvardxplus.harvard.edu/',
    'MITProfessionalX': u'https://{}payments.mitprofessionalx-stage.mit.edu/'
}

# BASIC raw URL
RAW_URL = {
    'HarvardMedGlobalAcademy':
        u'https://{}globalacademy-stage.hms.harvard.edu/',
    'HarvardXPLUS': u'https://{}stage-courses.harvardxplus.harvard.edu/',
    'MITProfessionalX': u'https://{}mitprofessionalx-stage.mit.edu/'
}

# E-commerce urls
ECOMMERCE_URL_WITHOUT_AUTH = RAW_ECOMMERCE_URL[ORG].format("")

ECOMMERCE_URL_WITH_AUTH = RAW_ECOMMERCE_URL[ORG].format(BASIC_AUTH)

# BASIC URLs
URL_WITHOUT_AUTH = RAW_URL[ORG].format("")

URL_WITH_AUTH = RAW_URL[ORG].format(BASIC_AUTH)

ECOMMERCE_API_URL = ECOMMERCE_URL_WITHOUT_AUTH + 'api/v2/'

ENROLLMENT_API_URL = URL_WITHOUT_AUTH + 'api/enrollment/v1'

CYBERSOURCE_CHECKOUT_URL = \
    u'https://testsecureacceptance.cybersource.com/checkout'

PROF_COURSE_ID = u'course-v1:{}+RTX_101+2016_02'.format(ORG)

PROF_COURSE_TITLE = u'{} Regression Test'.format(ORG)

PROF_COURSE_PRICE = 167.0

EMAIL_SENDER_ACCOUNTS = {
    'HarvardMedGlobalAcademy': 'hmsga-support@edx.org',
    'HarvardXPLUS': 'hxplus-support@edx.org',
    'MITProfessionalX': 'mitprofessionalx@mit.edu',
}

EMAIL_SENDER_ACCOUNT = EMAIL_SENDER_ACCOUNTS[ORG]

LOGO_LINKS = {
    'HarvardMedGlobalAcademy': 'hms-logo',
    'HarvardXPLUS': 'harvardX-logo',
    'MITProfessionalX': 'mit-prof-logo'
}

LOGO_LINK = LOGO_LINKS[ORG]

LOGO_ALT_TEXTS = {
    'HarvardMedGlobalAcademy': 'HMS Logo',
    'HarvardXPLUS': 'HarvardX Logo',
    'MITProfessionalX': 'MIT Logo'
}

LOGO_ALT_TEXT = LOGO_ALT_TEXTS[ORG]

SOCIAL_MEDIA_LINKS = {
    'HarvardMedGlobalAcademy': [
        'https://www.facebook.com/HarvardMed',
        'https://twitter.com/harvardmed',
        'https://www.linkedin.com/edu/harvard-medical-school-18482',
        'https://instagram.com/harvardmed/?hl=en'
    ],
    'HarvardXPLUS': [
        'https://www.facebook.com/HarvardX-187429968296722/',
        'https://twitter.com/harvardonline'
    ],
    'MITProfessionalX': [
        'https://www.facebook.com/MITProfessionalEducation',
        'https://twitter.com/mitprofessional',
        'https://www.linkedin.com/groups/73833/profile',
        'https://www.youtube.com/user/MITProfessionalEd'
    ]
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
BILLING_INFO = {
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
PAYMENT_DETAILS = {
    'card_number': '4111111111111111',
    'cvn': '123',
    'expiry_month': '07',
    'expiry_year': '2018'
}

# Existing user email
EXISTING_USER_EMAIL = 'wl_smoke_user01@example.com'

# Staff user email
STAFF_EMAIL = os.environ['STAFF_USER_EMAIL']

# Student user email
VISUAL_USER_EMAIL = 'wl_visual_test01@example.com'

# Default Threshold for visual difference
DIFF_THRESHOLD = 5000

# Timeouts
DEFAULT_TIMEOUT = 30

TIME_OUT_LIMIT = 90

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

SELECTED_COUNTRY = u'Pakistan'

SELECTED_LANGUAGE = u'Urdu'
