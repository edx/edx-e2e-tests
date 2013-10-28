import os

# Get the hostname of the edxapp instance from the environment 
EDXAPP_HOST = os.environ.get('EDXAPP_HOST')
BASE_URL = "http://" + EDXAPP_HOST
