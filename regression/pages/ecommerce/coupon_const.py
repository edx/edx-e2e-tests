# -*- coding: utf-8 -*-
"""
Constant used in coupon tests
"""
from datetime import datetime, timedelta

from regression.pages.whitelabel.const import ORG

# Coupon Error messages on basket page

EXPIRED_CODE_ERROR = "Coupon code '{}' has expired."

FUTURE_CODE_ERROR = "Coupon code '{}' has expired."

SINGLE_USE_CODE_REUSE_ERROR = "Coupon code '{}' has already been redeemed."

ONCE_PER_CUSTOMER_CODE_MAX_LIMIT = \
    'Your basket does not qualify for a coupon code discount.'

ONCE_PER_CUSTOMER_CODE_SAME_USER_REUSE = "Coupon code '{}' is invalid."

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

SINGLE_COURSE_CATALOG_TYPE = 'Single course'

DISCOUNT_COUPON_TYPE = 'Discount code'

DEFAULT_FIXED_BENEFIT_VALUE = 60

DEFAULT_PERCENTAGE_BENEFIT_VALUE = 40

ENROLLMENT_COUPON_TYPE = 'Enrollment code'

ABSOLUTE_BENEFIT_TYPE = 'Absolute'

PERCENTAGE_BENEFIT_TYPE = 'Percentage'

SINGLE_USE_VOUCHER_TYPE = 'Single use'

ONCE_PER_CUSTOMER_VOUCHER_TYPE = 'Once per customer'

STOCK_RECORD_IDS = {
    'HarvardMedGlobalAcademy': [8398],
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
    'HarvardMedGlobalAcademy': {
        'course-v1:HarvardMedGlobalAcademy+HMGA01+2016': 100.0,
        'course-v1:HarvardMedGlobalAcademy+HMGA02+2016': 100.0,
        'course-v1:HarvardMedGlobalAcademy+HMGA03+2016': 200.0,
        'course-v1:HarvardMedGlobalAcademy+HMGA04+2016': 200.0,
        'course-v1:HarvardMedGlobalAcademy+HMGA05+2016': 300.0,
        'course-v1:HarvardMedGlobalAcademy+HMGA06+2016': 300.0
    },
    'HarvardXPLUS': {
        'course-v1:MITProfessionalX+MITPX01+2016': 100.0,
        'course-v1:MITProfessionalX+MITPX02+2016': 100.0,
        'course-v1:MITProfessionalX+MITPX03+2016': 200.0,
        'course-v1:MITProfessionalX+MITPX04+2016': 200.0,
        'course-v1:MITProfessionalX+MITPX05+2016': 300.0,
        'course-v1:MITProfessionalX+MITPX06+2016': 300.0,
    },
    'MITProfessionalX': {
        'course-v1:HarvardXPLUS+HXP01+2016 ': 100.0,
        'course-v1:HarvardXPLUS+HXP02+2016 ': 100.0,
        'course-v1:HarvardXPLUS+HXP03+2016 ': 200.0,
        'course-v1:HarvardXPLUS+HXP04+2016 ': 200.0,
        'course-v1:HarvardXPLUS+HXP05+2016 ': 300.0,
        'course-v1:HarvardXPLUS+HXP06+2016 ': 300.0
    }
}
