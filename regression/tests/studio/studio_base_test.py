"""
Base class for all tests in studio
"""
from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.course_info_studio import (
    CourseUpdatesPageExtended
)
from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.pages.studio.grading_studio import GradingPageExtended
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.pages_page_studio import PagesPageExtended
from regression.pages.studio.studio_textbooks import TextbookPageExtended
from regression.tests.helpers import StudioLoginApi, get_course_info


class BaseTestClassNoCleanup(WebAppTest):
    """ Base class for all tests in studio """
    def setUp(self):
        super(BaseTestClassNoCleanup, self).setUp()


class StudioBaseTestClass(BaseTestClassNoCleanup):
    """
    Base class for all tests in studio with generic
    course setup and teardown.
    """
    def setUp(self):
        super(StudioBaseTestClass, self).setUp()
        self.addCleanup(self.clean_up_function)

    def clean_up_function(self):
        """
        Clean up function to clean the course
        """
        super(StudioBaseTestClass, self).tearDown()
        course_info = get_course_info()

        pages_page = PagesPageExtended(
            self.browser,
            course_info['org'],
            course_info['number'],
            course_info['run']
        )

        course_update_page = CourseUpdatesPageExtended(
            self.browser,
            course_info['org'],
            course_info['number'],
            course_info['run']
        )

        grading_page = GradingPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )

        studio_course_outline = CourseOutlinePageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )

        textbook_page = TextbookPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        login_api = StudioLoginApi()
        login_api.authenticate(self.browser)

        pages_page.visit()
        if pages_page.get_custom_page_count() > 0:
            pages_page.wait_for_the_visibility_of_new_page()
            pages_page.delete_all_pages()

        if pages_page.toggle_wiki_page_show_value() is False:
            pages_page.toggle_wiki_page_display()
            self.assertTrue(pages_page.toggle_wiki_page_show_value())

        course_update_page.visit()
        course_update_page.delete_all_course_updates()

        grading_page.visit()
        grading_page.remove_all_grades()
        grading_page.delete_all_assignment_types()

        studio_course_outline.visit()
        studio_course_outline.make_sure_only_one_section_is_present()

        textbook_page.visit()
        textbook_page.delete_all_textbooks()
