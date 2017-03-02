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

LOGIN_BASE_URL = 'https://{}:{}@{}'.format(
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, LMS_BASE_URL
)

LMS_REDIRECT_URL = 'https://stage.edx.org'
