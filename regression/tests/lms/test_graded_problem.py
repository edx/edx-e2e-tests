"""
End to end tests for submitting a graded problem.
"""
from __future__ import absolute_import

from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.course_page_lms import CourseHomePageExtended
from regression.pages.lms.lms_courseware import CoursewarePageExtended
from regression.pages.lms.utils import get_course_key
from regression.pages.studio.import_course_page import ImportCoursePageExtended
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_info


class GradedProblemTest(WebAppTest):
    """
    Regression tests on submitting a graded problem
    """
    tarball_name = 'course.tar.gz'

    def setUp(self):
        super(GradedProblemTest, self).setUp()

        login_api = LmsLoginApi()
        login_api.authenticate(self.browser)

        self.course_info = get_course_info()

        self.lms_courseware = CoursewarePageExtended(
            self.browser,
            get_course_key(self.course_info)
        )

        self.import_page = ImportCoursePageExtended(*self.page_args())
        self.import_page.visit()
        self.import_page.upload_tarball(self.tarball_name)
        self.import_page.wait_for_upload()

        self.course_page = CourseHomePageExtended(
            self.browser,
            get_course_key(self.course_info)
        )
        self.course_page.visit()

    def page_args(self):
        """
        Common arguments for pages to be used in tests.
        """
        return [
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        ]

    def test_graded_problem(self):
        """
        Verifies submission of a graded problem
        """
        self.course_page.click_resume_button()
        self.lms_courseware.wait_for_page()
        self.lms_courseware.submit_graded_problem()
