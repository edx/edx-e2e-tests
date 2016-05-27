import os

from regression.pages import AUTH_USER_NAME, AUTH_USER_PASSWORD

login_base_url = 'https://{}:{}@courses.stage.edx.org'.format(AUTH_USER_NAME, AUTH_USER_PASSWORD)
BASE_URL = os.environ.get('test_url', login_base_url)
