"""
URLs and constants for enterprise stuff
"""

from __future__ import absolute_import

import os

ENTERPRISE_PORTAL_LOGIN_URL = u"https://pmsalesdemo8.successfactors.com/login?company=SFPART011327#/login"

DEFAULT_ENTERPRISE_NAME = 'SuccessFactors'

ENTERPRISE_NAME = os.environ.get('ENTERPRISE_NAME', DEFAULT_ENTERPRISE_NAME)

DEFAULT_IDP_CSS_ID = 'bestrun'

IDP_CSS_ID = os.environ.get('IDP_CSS_ID', DEFAULT_IDP_CSS_ID)

ENT_CUSTOMER_UUID = os.environ.get('ENT_CUSTOMER_UUID', '')

ENT_CUSTOMER_CATALOG_UUID = os.environ.get('ENT_CUSTOMER_CATALOG_UUID',)

ENT_COURSE_ID = os.environ.get('ENT_COURSE_ID', 'course-v1:Mattx+TCE2E+2018')

ENT_PORTAL_USERNAME = os.environ.get('ENT_PORTAL_USERNAME')

ENT_PORTAL_PASSWORD = os.environ.get('ENT_PORTAL_PASSWORD')

ENT_PORTAL_EDX_LINKED_USERNAME = os.environ.get('ENT_PORTAL_EDX_LINKED_USERNAME')

ENT_PORTAL_EDX_LINKED_PASSWORD = os.environ.get('ENT_PORTAL_EDX_LINKED_PASSWORD')

ENT_COURSE_TITLE = os.environ.get('ENT_COURSE_TITLE')

ENT_COURSE_ORG = os.environ.get('ENT_COURSE_ORG')

ENT_COURSE_PRICE = os.environ.get('ENT_COURSE_PRICE')

ENT_COURSE_START_DATE = os.environ.get('ENT_COURSE_START_DATE')

DEFAULT_COURSE_PRICE = 100.0
