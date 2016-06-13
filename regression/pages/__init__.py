"""
This module retrieves a couple of environment variables
which later on are used by pages inside pages package.
"""

import os

BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USER', 'not_set')
BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', 'not_set')
