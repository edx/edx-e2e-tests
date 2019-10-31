"""
Some environment vars for WL tests
Here we are finalizing the target url based on test environment and org
"""

from __future__ import absolute_import

import os
from datetime import datetime

from regression.pages import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME

# Specify environment if stage is not used
DEFAULT_ENV = "stage"
TEST_ENV = os.environ.get("TEST_ENV", DEFAULT_ENV)

# Select the Org for which to run the tests
DEFAULT_ORG = 'MITxPRO'

ORG = os.environ.get('ORG', DEFAULT_ORG)

SANDBOX_AND_DEVSTACK_ECOM_PREFIX = "ecommerce-"
STAGE_ECOM_PREFIX = "payments."

BASE_URL = ""
ECOM_PREFIX = ""
ECOM_URL = ""
LMS_URL_WITH_AUTH = ""
ECOM_URL_WITH_AUTH = ""

# Devstack handles course orgs differently, we use this to map the
# orgs to course orgs. Other environments use the default ORG below.
ORG_COURSE_ORG_MAP = {}

LMS_PROTOCOL = os.environ.get('LMS_PROTOCOL', 'https')


def get_base_service_urls(base_url, ecom_prefix, ecom_base_url):
    """
    Handles string formatting the urls correctly for ECOM_URL,
    LMS_URL_WITH_AUTH, and ECOM_URL_WITH_AUTH
    """
    basic_auth_str = ''
    if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
        basic_auth_str = '{}:{}@'.format(
            BASIC_AUTH_USERNAME,
            BASIC_AUTH_PASSWORD
        )

    ecom_url = '{}://{}{}'.format(
        LMS_PROTOCOL,
        ecom_prefix,
        ecom_base_url
    )

    lms_url_with_auth = '{}://{}{}'.format(
        LMS_PROTOCOL,
        basic_auth_str,
        base_url
    )

    ecom_url_with_auth = '{}://{}{}{}'.format(
        LMS_PROTOCOL,
        basic_auth_str,
        ecom_prefix,
        ecom_base_url
    )

    return ecom_url, lms_url_with_auth, ecom_url_with_auth


if TEST_ENV in (DEFAULT_ENV, "sandbox"):
    if TEST_ENV == DEFAULT_ENV:
        BASE_URLS = {
            'edX': u'courses.stage.edx.org',
            'HarvardMedGlobalAcademy': u'stage.cmeonline.hms.harvard.edu',
            'MITxPRO': u'stage.MITxPRO.mit.edu'
        }

        ECOM_PREFIX = STAGE_ECOM_PREFIX
    else:
        # Get DNS name if tests are running on sandbox
        TARGET_DNS = os.environ.get("TARGET_DNS")
        BASE_URLS = {
            'Enterprise': "{}.sandbox.edx.org".format(TARGET_DNS),
            'MITxPRO': "mitxpro-{}.sandbox.edx.org".format(TARGET_DNS),
            'Harvard': "hms-{}.sandbox.edx.org".format(TARGET_DNS)
        }
        ECOM_PREFIX = SANDBOX_AND_DEVSTACK_ECOM_PREFIX

    BASE_URL = BASE_URLS[ORG]

    # In this case BASE_URL and ECOM_BASE_URL are the same intentionally
    ECOM_URL, LMS_URL_WITH_AUTH, ECOM_URL_WITH_AUTH = get_base_service_urls(
        BASE_URL,
        ECOM_PREFIX,
        BASE_URL
    )

    if ORG == 'HarvardMedGlobalAcademy' and TEST_ENV == DEFAULT_ENV:
        ECOM_URL = "{}://{}".format(
            LMS_PROTOCOL,
            'stage-payments.cmeonline.hms.harvard.edu'
        )

elif TEST_ENV == "devstack":
    # Get DNS name if tests are running on devstack
    BASE_URLS = {
        'edX': u"edx-wl-ci.e2e.devstack:18000",
        'MITxPRO': u"mitxpro-wl-ci.e2e.devstack:18000",
        'Harvard': u"hms-wl-ci.e2e.devstack:18000",
        'HarvardMedGlobalAcademy': u'globalacademy-wl-ci.e2e.devstack:18000',
    }
    BASE_URL = BASE_URLS[ORG]
    ECOM_BASE_URL = BASE_URL.replace('18000', '18130')

    ECOM_URL, LMS_URL_WITH_AUTH, ECOM_URL_WITH_AUTH = get_base_service_urls(
        BASE_URL,
        SANDBOX_AND_DEVSTACK_ECOM_PREFIX,
        ECOM_BASE_URL
    )

    ORG_COURSE_ORG_MAP = {
        'edX': 'edx',
        'MITxPRO': 'mitpe',
        'Harvard': 'hms',
        'HarvardMedGlobalAcademy': 'globalacademy'
    }
else:
    raise Exception("Unknown TEST_ENV '{}'".format(TEST_ENV))

LMS_URL = '{}://{}'.format(LMS_PROTOCOL, BASE_URL)

# Get Course ID, Price and Name
DEFAULT_COURSE_NUM = "WL_E2E"
DEFAULT_COURSE_RUN = "2018"

# This line can be confusing, but the order of setting this is:
# 1- The COURSE_ORG environment variable
# 2- The ORG_COURSE_ORG_MAP for the local ORG, only relevant in devstack
# 3- The local ORG
COURSE_ORG = os.environ.get("COURSE_ORG", ORG_COURSE_ORG_MAP.get(ORG, ORG))
COURSE_NUMBER = os.environ.get("COURSE_NUMBER", DEFAULT_COURSE_NUM)
COURSE_RUN = os.environ.get("COURSE_RUN", DEFAULT_COURSE_RUN)
DEFAULT_COURSE_PRICE = 167.0
