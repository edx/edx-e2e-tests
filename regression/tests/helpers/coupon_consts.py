"""
Constant used in coupon tests
"""
from datetime import datetime, timedelta

from regression.pages.whitelabel.const import ORG

# Coupon Error messages on basket page

EXPIRED_CODE_ERROR = "Coupon code '{}' has expired."

FUTURE_CODE_ERROR = "Coupon code '{}' is not active."

SINGLE_USE_CODE_REUSE_ERROR = "Coupon code '{}' has already been redeemed."

ONCE_PER_CUSTOMER_CODE_MAX_LIMIT = \
    'Your basket does not qualify for a coupon code discount.'

ONCE_PER_CUSTOMER_CODE_SAME_USER_REUSE = \
    "You have already used this coupon in a previous order"

INVALID_DOMAIN_ERROR_MESSAGE_ON_BASKET = \
    'Your basket does not qualify for a coupon code discount.'

# Coupon Error messages on redeem url page

EXPIRED_REDEEM_URL_ERROR = 'This coupon code has expired.'

FUTURE_REDEEM_URL_ERROR = 'This coupon code is not yet valid.'

SINGLE_USE_REDEEM_URL_REUSE_ERROR = 'This coupon has already been used'

ONCE_PER_CUSTOMER_REDEEM_URL_MAX_LIMIT = \
    'This coupon code is no longer available.'

ONCE_PER_CUSTOMER_REDEEM_URL_SAME_USER_REUSE = \
    'You have already used this coupon in a previous order'

INVALID_DOMAIN_ERROR_MESSAGE_ON_REDEEM_URL = \
    'You are not eligible to use this coupon.'

INACTIVE_ACCOUNT_ERROR_MESSAGE = \
    'You need to activate your account in order to redeem this coupon.'

# Coupons info

DEFAULT_START_DATE = (datetime.today() -
                      timedelta(days=15)).strftime('%Y-%m-%dT%H:%M:%SZ')

EXPIRED_END_DATE = (datetime.today() -
                    timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%SZ')

DEFAULT_END_DATE = (datetime.today() +
                    timedelta(days=15)).strftime('%Y-%m-%dT%H:%M:%SZ')

FUTURE_START_DATE = (datetime.today() +
                     timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%SZ')

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

STOCK_RECORD_IDS = {
    'HarvardMedGlobalAcademy': [7900],
    'HarvardXPLUS': [8396],
    'MITProfessionalX': [8400],
}

STOCK_RECORD_ID = STOCK_RECORD_IDS[ORG]

# Coupon users

COUPON_USERS = {
    'coupon_user_01': 'wl_coupon_user01@example.com',
    'coupon_user_02': 'wl_coupon_user02@example.com',
    'coupon_user_03': 'wl_coupon_user03@example.com'
}

VALID_DOMAIN_USERS = {
    'coupon_user_04': 'wl_coupon_user04@emaildomainfour.com',
    'coupon_user_05': 'wl_coupon_user05@emaildomainfive.com'
}

INVALID_DOMAIN_USERS = {
    'coupon_user_06': 'wl_coupon_user06@emaildomainsix.com',
    'coupon_user_07': 'wl_coupon_user07@emaildomainseven.com'
}

# Email domains

VALID_EMAIL_DOMAINS = "emaildomainfour.com,emaildomainfive.com"

# Courses for dynamic coupons testing
COUPON_COURSES = {
    u'HarvardMedGlobalAcademy': {
        u'course-v1:HarvardMedGlobalAcademy+HMGA01+2016': {
            'price': 100.0, 'title': u'Automated Tests-HMGA01'
        },
        u'course-v1:HarvardMedGlobalAcademy+HMGA02+2016': {
            'price': 100.0, 'title': u'Automated Tests-HMGA02'
        },
        u'course-v1:HarvardMedGlobalAcademy+HMGA03+2016': {
            'price': 200.0, 'title': u'Automated Tests-HMGA03'
        },
        u'course-v1:HarvardMedGlobalAcademy+HMGA04+2016': {
            'price': 200.0, 'title': u'Automated Tests-HMGA04'
        },
        u'course-v1:HarvardMedGlobalAcademy+HMGA05+2016': {
            'price': 300.0, 'title': u'Automated Tests-HMGA05'
        },
        u'course-v1:HarvardMedGlobalAcademy+HMGA06+2016': {
            'price': 300.0, 'title': u'Automated Tests-HMGA06'
        }
    },
    u'MITProfessionalX': {
        u'course-v1:MITProfessionalX+MITPX01+2016': {
            'price': 100.0, 'title': u'Automated Tests-MITPX01'
        },
        u'course-v1:MITProfessionalX+MITPX02+2016': {
            'price': 100.0, 'title': u'Automated Tests-MITPX02'
        },
        u'course-v1:MITProfessionalX+MITPX03+2016': {
            'price': 200.0, 'title': u'Automated Tests-MITPX03'
        },
        u'course-v1:MITProfessionalX+MITPX04+2016': {
            'price': 200.0, 'title': u'Automated Tests-MITPX04'
        },
        u'course-v1:MITProfessionalX+MITPX05+2016': {
            'price': 300.0, 'title': u'Automated Tests-MITPX05'
        },
        u'course-v1:MITProfessionalX+MITPX06+2016': {
            'price': 300.0, 'title': u'Automated Tests-MITPX06'
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
        },
        u'course-v1:HarvardXPLUS+HXP04+2016': {
            'price': 200.0, 'title': u'Automated Tests-HXP04'
        },
        u'course-v1:HarvardXPLUS+HXP05+2016': {
            'price': 300.0, 'title': u'Automated Tests-HXP05'
        },
        u'course-v1:HarvardXPLUS+HXP06+2016': {
            'price': 300.0, 'title': u'Automated Tests-HXP06'
        }
    }
}

COURSES_CATALOG = COUPON_COURSES[ORG]

COURSES_CATALOG_QUERIES = {
    'MITProfessionalX': 'org:MITProfessionalX and number:MITPX*',
    'HarvardXPLUS': 'org:HarvardXPLUS and number:HXP*',
    'HarvardMedGlobalAcademy': 'org:HarvardMedGlobalAcademy and number:HMGA*'
}

CATALOG_QUERY = COURSES_CATALOG_QUERIES[ORG]
