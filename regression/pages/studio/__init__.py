"""
Create base url for studio page objects.
While creating the url, basic authentication
username and basic authentication password
should be used.
"""

import os

from regression.pages import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

STUDIO_STAGE_BASE_URL = 'studio.stage.edx.org'
LMS_STAGE_BASE_URL = 'courses.stage.edx.org'

EDXAPP_CMS_DOC_LINK_BASE_URL = os.environ.get(
    'EDXAPP_CMS_DOC_LINK_BASE_URL',
    'https://edx.readthedocs.io/projects/edx-partner-course-staff')

LMS_BASE_URL = os.environ.get('LMS_BASE_URL', LMS_STAGE_BASE_URL)
LMS_PROTOCOL = os.environ.get('LMS_PROTOCOL', 'https')

STUDIO_BASE_URL = os.environ.get('STUDIO_BASE_URL', STUDIO_STAGE_BASE_URL)
STUDIO_PROTOCOL = os.environ.get('STUDIO_PROTOCOL', 'https')

if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
    LOGIN_BASE_URL = '{}://{}:{}@{}'.format(
        STUDIO_PROTOCOL, BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD,
        STUDIO_BASE_URL)
    LMS_LOGIN_BASE_URL = '{}://{}:{}@{}'.format(
        LMS_PROTOCOL, BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD,
        LMS_BASE_URL)
else:
    LOGIN_BASE_URL = '{}://{}'.format(STUDIO_PROTOCOL, STUDIO_BASE_URL)
    LMS_LOGIN_BASE_URL = '{}://{}'.format(LMS_PROTOCOL, LMS_BASE_URL)
