import os

from regression.pages import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD

login_base_url = 'https://{}:{}@studio.stage.edx.org'.format(
    BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)
BASE_URL = os.environ.get('test_url', login_base_url)
