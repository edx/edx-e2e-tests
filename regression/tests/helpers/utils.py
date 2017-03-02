"""
Test helper functions.
"""
import os

from regression.pages.studio.utils import get_course_key
from regression.pages.studio import LOGIN_BASE_URL

COURSE_ORG = 'COURSE_ORG'
COURSE_NUMBER = 'COURSE_NUMBER'
COURSE_RUN = 'COURSE_RUN'
COURSE_DISPLAY_NAME = 'COURSE_DISPLAY_NAME'


def get_course_info():
    """
    Returns the course info of the course that we use for
    the regression tests.
    """
    return {
        'org': os.environ.get(COURSE_ORG),
        'number': os.environ.get(COURSE_NUMBER),
        'run': os.environ.get(COURSE_RUN),
        'display_name': os.environ.get(
            COURSE_DISPLAY_NAME)
    }


def get_course_display_name():
    """
    Returns the course info of the course that we use for
    the regression tests.
    """
    return os.environ.get(COURSE_DISPLAY_NAME)


def visit_all(pages):
    """
    Visit each page object in `pages` (an iterable).
    """
    for page in pages:
        print "Visiting: {}".format(page)
        page.visit()


def get_url(url_path, course_info):
    """
    Construct a URL to the page within the course.
    """
    course_key = get_course_key(course_info)
    return "/".join([LOGIN_BASE_URL, url_path, unicode(course_key)])


def get_data_locator(page):
    """
    Returns:
        Unique data locator for the component
    """
    data_locator = page.q(css='.hd-3').attrs('id')[0]
    return data_locator


def get_data_id_of_component(page):
    """
    Returns:
        ID for the component
    """
    data_id = page.q(css='.problem-header').attrs('id')[0]
    return data_id
