"""
Utility functions for lms page objects.
"""
import os
from opaque_keys.edx.locator import CourseLocator
from regression.pages.lms.login_lms import LmsLogin


def get_course_key(course_info, module_store='split'):
    """
    Returns the course key based upon course info passed.
    Course key depends upon the module store passed. The default
    module store is 'split'.
    """
    course_key = CourseLocator(
        course_info['org'],
        course_info['number'],
        course_info['run'],
        deprecated=(module_store == 'draft')
    )
    return unicode(course_key)


def workaround_login_redirect(page):
    """
    Temporary workaround while we investigate the root cause
    of the user being redirected to the login page. TE-2207
    """
    page.browser.get(page.url)
    if page.browser.current_url.find('/signin?next=') > 0:
        user = os.environ.get('USER_LOGIN_EMAIL')
        password = os.environ.get('USER_LOGIN_PASSWORD')
        login_page = LmsLogin(page.browser)
        login_page.provide_info(user, password)
        login_page.submit()
