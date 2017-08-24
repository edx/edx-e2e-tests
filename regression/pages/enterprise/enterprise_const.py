"""
URLs and constants for enterprise stuff
"""

import os


ENTERPRISE_PORTAL_LOGIN_URL = u"https://pmsalesdemo8.successfactors.com/" \
                              u"login?company=SFPART011327#/login"

DEFAULT_ENTERPRISE_NAME = 'SuccessFactors'

ENTERPRISE_NAME = os.environ.get('ENTERPRISE_NAME', DEFAULT_ENTERPRISE_NAME)

DEFAULT_IDP_CSS_ID = 'bestrun'

IDP_CSS_ID = os.environ.get('IDP_CSS_ID', DEFAULT_IDP_CSS_ID)
