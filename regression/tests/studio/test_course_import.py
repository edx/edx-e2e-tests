"""
Course import test
"""
from __future__ import absolute_import

from bok_choy.web_app_test import WebAppTest

from regression.pages.studio.course_outline_page import CourseOutlinePageExtended
from regression.pages.studio.import_course_page import ImportCoursePageExtended
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_info


class TestCourseImport(WebAppTest):
    """
    Tests the Course import page
    """
    tarball_name = 'course.tar.gz'
    import_page_class = ImportCoursePageExtended
    landing_page_class = CourseOutlinePageExtended

    def setUp(self):
        super(TestCourseImport, self).setUp()

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

        self.course_info = get_course_info()

        self.import_page = ImportCoursePageExtended(*self.page_args())
        self.course_outline_page = CourseOutlinePageExtended(*self.page_args())

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

    def test_course_updated(self):
        """
        Tests that we can update(import) course using tarball.
        """
        self.import_page.visit()
        self.import_page.upload_tarball(self.tarball_name)
        self.import_page.wait_for_upload()
        self.course_outline_page.visit()
        # There's a section named
        # 'Section :754c5e889ac3489e9947ba62b916bdab' in the tarball.
        self.assertIn(
            "Section :754c5e889ac3489e9947ba62b916bdab",
            self.course_outline_page.get_section_names()
        )
