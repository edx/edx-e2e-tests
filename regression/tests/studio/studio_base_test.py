"""
Base class for all tests in studio
"""
from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers import LoginHelper, get_course_info
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.pages_page_studio import PagesPageExtended
from regression.pages.studio.grading_studio import GradingPageExtended
from regression.pages.studio.studio_textbooks import TextbookPageExtended
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.studio.studio_rerun import StudioRerun
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.studio.asset_index_studio import AssetIndexPageExtended
from regression.pages.studio.course_info_studio import (
    CourseUpdatesPageExtended
)
from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)


class StudioBaseTestClass(WebAppTest):
    """
    Base class for all tests in studio
    """
    def setUp(self):
        super(StudioBaseTestClass, self).setUp()

        # Login to Lms first to avoid authentication problem
        self.lms_login_page = LmsLogin(self.browser)
        LoginHelper.login(self.lms_login_page)

        self.login_page = StudioLogin(self.browser)
        self.course_rerun_page = StudioRerun(self.browser)
        self.studio_home_page = DashboardPageExtended(self.browser)
        LoginHelper.login(self.login_page)
        self.studio_home_page.visit()
        self.studio_home_page.click_course_rerun()
        self.course_rerun_page.wait_for_page()
        self.course_rerun_page.add_rerun_with_run()
        self.studio_home_page.wait_for_page()
        self.browser.refresh()

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

        asset_page = AssetIndexPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )

        login_page = StudioLogin(self.browser)
        LoginHelper.login(login_page)
        pages_page.visit()
        if pages_page.get_custom_page_count() > 0:
            pages_page.wait_for_the_visibility_of_new_page()
            pages_page.delete_all_pages()

        if pages_page.is_page_configured_to_show() is False:
            pages_page.click_hide_show_toggle()
            self.assertTrue(pages_page.is_page_configured_to_show())

        course_update_page.visit()
        course_update_page.delete_all_course_updates()

        grading_page.visit()
        grading_page.remove_all_grades()
        grading_page.delete_all_assignment_types()

        studio_course_outline.visit()
        studio_course_outline.make_sure_only_one_section_is_present()

        textbook_page.visit()
        textbook_page.delete_all_textbooks()

        asset_page.visit()
        asset_count = asset_page.get_files_count()
        while asset_count != 0:
            asset_page.click_delete_file()
            asset_count = asset_page.get_files_count()
