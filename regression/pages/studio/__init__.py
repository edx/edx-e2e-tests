"""
Create base url for studio page objects.
While creating the url, basic authentication
username and basic authentication password
should be used.
"""

import os

from regression.pages import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

STUDIO_BASE_URL = os.environ.get('STUDIO_BASE_URL', 'studio.stage.edx.org')

LOGIN_BASE_URL = 'https://{}:{}@{}'.format(
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, STUDIO_BASE_URL)
