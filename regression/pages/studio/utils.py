"""
Utility functions for studio page objects.
"""
from opaque_keys.edx.locator import CourseLocator


def get_course_key(course_info, module_store='split'):
    """
    Returns the course key based upon course info passed.
    Course key depends upon the module store passed. The default
    module store is 'split'.
    """
    return CourseLocator(
        course_info['course_org'],
        course_info['course_num'],
        course_info['course_run'],
        deprecated=(module_store == 'draft')
    )
