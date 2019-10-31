"""
Create base url for lms page objects.
While creating the url, basic authentication
username and basic authentication password
should be used.
"""

from __future__ import absolute_import

import os

from regression.pages import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME

LMS_STAGE_BASE_URL = 'courses.stage.edx.org'
# LMS_SANDBOX_BASE_URL = 'business.sandbox.edx.org'
ECOM_STAGE_BASE_URL = 'ecommerce.stage.edx.org'
# ECOM_SANDBOX_BASE_URL = 'ecommerce-business.sandbox.edx.org'

LMS_BASE_URL = os.environ.get('LMS_BASE_URL', LMS_STAGE_BASE_URL)
ECOM_BASE_URL_STR = os.environ.get('ECOM_STAGE_BASE_URL', ECOM_STAGE_BASE_URL)
LMS_PROTOCOL = os.environ.get('LMS_PROTOCOL', 'https')

if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
    LOGIN_BASE_URL = '{}://{}:{}@{}'.format(
        LMS_PROTOCOL, BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LMS_BASE_URL
    )
    ECOM_BASE_URL = '{}://{}:{}@{}'.format(
        LMS_PROTOCOL, BASIC_AUTH_USERNAME,
        BASIC_AUTH_PASSWORD, ECOM_BASE_URL_STR
    )
else:
    LOGIN_BASE_URL = '{}://{}'.format(LMS_PROTOCOL, LMS_BASE_URL)
    ECOM_BASE_URL = '{}://{}'.format(LMS_PROTOCOL, ECOM_BASE_URL_STR)

LMS_REDIRECT_URL = 'https://stage.edx.org'
