"""
Create base url for studio page objects.
While creating the url, basic authentication
username and basic authentication password
should be used.
"""

import os

from regression.pages import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

LOGIN_BASE_URL = 'https://{}:{}@studio.stage.edx.org'.format(
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)
BASE_URL = os.environ.get('test_url', LOGIN_BASE_URL)
