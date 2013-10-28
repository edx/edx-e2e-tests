import os

# Get the hostname of the edxapp instance from the environment
MKTG_HOST = os.environ.get('MKTG_HOST')
BASE_URL = "https://" + MKTG_HOST
