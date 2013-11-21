import os

# Get the hostname of the instance from the environment
BASE_URL = "{0}://{1}".format(os.environ['cms_protocol'], os.environ['cms_test_host'])
