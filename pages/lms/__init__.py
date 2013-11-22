import os

# Get the hostname of the instance from the environment
BASE_URL = "{0}://{1}".format(os.environ['lms_protocol'], os.environ['lms_test_host'])
