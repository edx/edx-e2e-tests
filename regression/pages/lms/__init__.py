"""
Create base url for lms page objects.
While creating the url, basic authentication
username and basic authentication password
should be used.
"""

import os

from regression.pages import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

LMS_STAGE_BASE_URL = 'courses.stage.edx.org'

LMS_BASE_URL = os.environ.get('LMS_BASE_URL', LMS_STAGE_BASE_URL)
LMS_PROTOCOL = os.environ.get('LMS_PROTOCOL', 'https')

if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
    LOGIN_BASE_URL = '{}://{}:{}@{}'.format(
        LMS_PROTOCOL, BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LMS_BASE_URL
    )
else:
    LOGIN_BASE_URL = '{}://{}'.format(LMS_PROTOCOL, LMS_BASE_URL)

LMS_REDIRECT_URL = 'https://stage.edx.org'
