"""
Some environment vars for WL tests
Here we are finalizing the target url based on test environment and org
"""

import os

from datetime import datetime

from regression.pages import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD


# Specify environment if stage is not used
DEFAULT_ENV = "stage"
TEST_ENV = os.environ.get("TEST_ENV", DEFAULT_ENV)

# Select the Org for which to run the tests
DEFAULT_ORG = 'MITxPRO'

ORG = os.environ.get('ORG', DEFAULT_ORG)

SANDBOX_ECOM_PREFIX = "ecommerce-"
STAGE_ECOM_PREFIX = "payments."

BASE_URL = ""
ECOM_PREFIX = ""

if TEST_ENV == DEFAULT_ENV:
    BASE_URLS = {
        'edX': u'courses.stage.edx.org',
        'HarvardMedGlobalAcademy': u'globalacademy-stage.hms.harvard.edu',
        'MITxPRO': u'stage.MITxPRO.mit.edu'
    }

    BASE_URL = BASE_URLS[ORG]
    ECOM_PREFIX = STAGE_ECOM_PREFIX

elif TEST_ENV == "sandbox":
    # Get DNS name if tests are running on sandbox
    TARGET_DNS = os.environ.get("TARGET_DNS")
    BASE_URLS = {
        'MITxPRO': "mitxpro-{}.sandbox.edx.org".format(TARGET_DNS),
        'Harvard': "hms-{}.sandbox.edx.org".format(TARGET_DNS)
    }
    BASE_URL = BASE_URLS[ORG]
    ECOM_PREFIX = SANDBOX_ECOM_PREFIX


LMS_PROTOCOL = os.environ.get('LMS_PROTOCOL', 'https')


LMS_URL = '{}://{}'.format(LMS_PROTOCOL, BASE_URL)
ECOM_URL = '{}://{}{}'.format(
    LMS_PROTOCOL,
    ECOM_PREFIX,
    BASE_URL
)

if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
    LMS_URL_WITH_AUTH = '{}://{}:{}@{}'.format(
        LMS_PROTOCOL, BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, BASE_URL
    )
    ECOM_URL_WITH_AUTH = '{}://{}:{}@{}{}'.format(
        LMS_PROTOCOL,
        BASIC_AUTH_USERNAME,
        BASIC_AUTH_PASSWORD,
        ECOM_PREFIX,
        BASE_URL
    )
else:
    LMS_URL_WITH_AUTH = '{}://{}'.format(LMS_PROTOCOL, BASE_URL)
    ECOM_URL_WITH_AUTH = '{}://{}{}'.format(
        LMS_PROTOCOL,
        ECOM_PREFIX,
        BASE_URL
    )


# Get Course ID, Price and Name
DEFAULT_COURSE_NUM = "WL_E2E"
DEFAULT_COURSE_RUN = str(datetime.now().year)
COURSE_ORG = os.environ.get("COURSE_ORG", ORG)
COURSE_NUMBER = os.environ.get("COURSE_NUMBER", DEFAULT_COURSE_NUM)
COURSE_RUN = os.environ.get("COURSE_RUN", DEFAULT_COURSE_RUN)
DEFAULT_COURSE_PRICE = 167.0
