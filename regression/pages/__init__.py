"""
This module retrieves a couple of environment variables
which later on are used by pages inside pages package.
"""

from __future__ import absolute_import

import os

BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USER', 'not_set')
BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD', 'not_set')

LOGIN_EMAIL = os.environ.get('USER_LOGIN_EMAIL', 'not_set')
LOGIN_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD', 'not_set')

UPLOAD_FILE_DIR = os.environ.get('UPLOAD_FILE_DIR')
