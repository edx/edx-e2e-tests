"""
URLs and constants for enterprise stuff
"""

import os


DEFAULT_IDP_URL = u"https://idp.testshib.org/idp/Authn/UserPassword"

IDP_URL = os.environ.get('IDP_URL', DEFAULT_IDP_URL)

DEFAULT_IDP_NAME = "TestShib"

IDP_NAME = os.environ.get('IDP_NAME', DEFAULT_IDP_NAME)

DEFAULT_ENTERPRISE_NAME = 'TestDemoEnterprise'

ENTERPRISE_NAME = os.environ.get('ENTERPRISE_NAME', DEFAULT_ENTERPRISE_NAME)

DEFAULT_IDP_CSS_ID = 'arbi-test-shib'

IDP_CSS_ID = os.environ.get('IDP_CSS_ID', DEFAULT_IDP_CSS_ID)
