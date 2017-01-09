"""
Studio Course Rerun page
"""
import os
from uuid import uuid4
from bok_choy.page_object import PageObject
from regression.pages.studio import BASE_URL
from regression.tests.helpers import get_course_info
from regression.pages.lms.utils import get_course_key


class StudioRerun(PageObject):
    """
    Studio Course Rerun for Manual Smoke Test Course
    """
    course_details = get_course_key(get_course_info())
    url = BASE_URL + '/course_rerun/' + course_details

    def is_browser_on_page(self):
        return self.q(css='.rerun-course-save.is-disabled').present

    def add_rerun_with_run(self):
        """
        Adds rerun with different Course Run
        """
        updated_run = 'Run{}'.format(uuid4().hex)
        self.q(css='#rerun-course-run').fill(updated_run)
        self.wait_for_element_visibility(
            '.rerun-course-save', 'Create Rerun button')
        self.q(css='.rerun-course-save').click()
        os.environ['COURSE_RUN'] = updated_run
