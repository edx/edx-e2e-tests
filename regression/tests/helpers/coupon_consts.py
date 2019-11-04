"""
Constant used in coupon tests
"""
from __future__ import absolute_import

from datetime import datetime, timedelta

from regression.pages.whitelabel.const import ORG

# Coupon Error messages on basket page

EXPIRED_CODE_ERROR = "Coupon code '{}' has expired."

FUTURE_CODE_ERROR = "Coupon code '{}' is not active."

SINGLE_USE_CODE_REUSE_ERROR = "Coupon code '{}' is not available. This coupon has already been used"

ONCE_PER_CUSTOMER_CODE_MAX_LIMIT = 'Your basket does not qualify for a coupon code discount.'

ONCE_PER_CUSTOMER_CODE_SAME_USER_REUSE = "You have already used this coupon in a previous order"

INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET = 'Your basket does not qualify for a coupon code discount.'

# Coupon Error messages on redeem url page

EXPIRED_REDEEM_URL_ERROR = 'This coupon code has expired.'

FUTURE_REDEEM_URL_ERROR = 'This coupon code is not yet valid.'

SINGLE_USE_REDEEM_URL_REUSE_ERROR = 'This coupon has already been used'

ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT = 'This coupon code is no longer available.'

ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE = 'You have already used this coupon in a previous order'

INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL = 'You are not eligible to use this coupon.'

INACTIVE_ACCOUNT_ERROR_MESSAGE = 'You need to activate your account in order to redeem this coupon.'

# Coupons info

DEFAULT_START_DATE = (datetime.today() - timedelta(days=15)).strftime('%Y-%m-%dT%H:%M:%SZ')

EXPIRED_END_DATE = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%SZ')

DEFAULT_END_DATE = (datetime.today() + timedelta(days=15)).strftime('%Y-%m-%dT%H:%M:%SZ')

FUTURE_START_DATE = (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%SZ')

COURSE_CATALOG_TYPE = {'single': 'Single course', 'multi': 'Multiple courses'}

SEAT_TYPE = {'prof': 'professional', 'ver': 'verified'}

COURSE_SEAT_TYPES = {'prof': ['professional']}

COUPON_TYPE = {'disc': 'Discount code', 'enroll': 'Enrollment code'}

BENEFIT_TYPE = {'abs': 'Absolute', 'per': 'Percentage'}

VOUCHER_TYPE = {
    'single': 'Single use',
    'once_per_cust': 'Once per customer',
    'multi': 'Multi-use'
}

BENEFIT_VALUE = {'fixed': 60, 'per': 40}

INVALID_DOMAIN_USERS = {
    'coupon_user_06': 'wl_coupon_user06@emaildomainsix.com',
    'coupon_user_07': 'wl_coupon_user07@emaildomainseven.com'
}

# Valid Email domain

VALID_EMAIL_DOMAIN = "example.com"

# Courses for dynamic coupons testing
COUPON_COURSES = {
    u'HarvardMedGlobalAcademy': {
        u'course-v1:HarvardMedGlobalAcademy+E2E02+2018': {
            'price': 200.0, 'title': u'HarvardMedGlobalAcademy-E2E-Test-2'
        },
        u'course-v1:HarvardMedGlobalAcademy+E2E03+2018': {
            'price': 300.0, 'title': u'HarvardMedGlobalAcademy-E2E-Test-3'
        },
        u'course-v1:HarvardMedGlobalAcademy+E2E04+2018': {
            'price': 400.0, 'title': u'HarvardMedGlobalAcademy-E2E-Test-4'
        }
    },
    u'MITxPRO': {
        u'course-v1:MITxPRO+E2E02+2018': {
            'price': 200.0, 'title': u'MITxPRO-E2E-Test-2'
        },
        u'course-v1:MITxPRO+E2E03+2018': {
            'price': 300.0, 'title': u'MITxPRO-E2E-Test-3'
        },
        u'course-v1:MITxPRO+E2E04+2018': {
            'price': 400.0, 'title': u'MITxPRO-E2E-Test-4'
        }
    },
    u'HarvardXPLUS': {
        u'course-v1:HarvardXPLUS+HXP01+2016': {
            'price': 100.0, 'title': u'Automated Tests-HXP01'
        },
        u'course-v1:HarvardXPLUS+HXP02+2016': {
            'price': 100.0, 'title': u'Automated Tests-HXP02'
        },
        u'course-v1:HarvardXPLUS+HXP03+2016': {
            'price': 200.0, 'title': u'Automated Tests-HXP03'
        }
    },
    u'Enterprise': {}
}

COURSES_CATALOG = COUPON_COURSES[ORG]

COURSES_CATALOG_QUERIES = {
    'Enterprise': '',
    'MITxPRO': 'org:MITxPRO and number:E2E*',
    'HarvardXPLUS': 'org:HarvardXPLUS and number:HXP*',
    'HarvardMedGlobalAcademy': 'org:HarvardMedGlobalAcademy and number:E2E*'
}

CATALOG_QUERY = COURSES_CATALOG_QUERIES[ORG]
