import os

username = os.environ.get('BASIC_AUTH_USER', 'not_set')
password = os.environ.get('BASIC_AUTH_PASSWORD', 'not_set')

login_base_url = 'https://{}:{}@courses.stage.edx.org'.format(username, password)
BASE_URL = os.environ.get('test_url', login_base_url)
