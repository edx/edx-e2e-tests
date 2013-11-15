import os

# Get the hostname of the instance from the environment
# These are guaranteed to be defined by the fabric commands
BASE_URL = "{0}://{1}".format(os.environ['protocol'], os.environ['test_host'])
