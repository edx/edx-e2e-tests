"""
Course pages test
"""
from uuid import uuid4
from flaky import flaky

from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers.api_clients import (
    StudioLoginApi, LmsLoginApi
)
from regression.tests.helpers.utils import get_course_info
from regression.pages.lms.utils import get_course_key
from regression.pages.studio.pages_page_studio import PagesPageExtended
from regression.pages.lms.course_page_lms import CourseInfoPageExtended
from regression.pages.lms.lms_courseware import CoursewarePageExtended


class CoursePagesTest(WebAppTest):
    """
    Course Pages test
    """
    def setUp(self):
        super(CoursePagesTest, self).setUp()
        self.course_info = get_course_info()

        login_api = StudioLoginApi()
        login_api.authenticate(self.browser)

        self.pages_page = PagesPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )

    def assert_page_has_been_added(self, initial_page_count):
        """
        Asserts that page has been added.

        Checks that page count in greater than that of before.
        Also ensures that page present at the last index
        doesn't have id as when new page is added it doesn't have
        any id associated with it.

        Arguments:
            initial_page_count (int): Page count before
            the addition of a new page.
        """
        current_page_count = self.pages_page.get_custom_page_count()
        self.assertGreater(
            current_page_count, initial_page_count
        )
        last_page_id = self.pages_page.q(
            css='.component.course-tab.is-movable'
        ).results[current_page_count - 1].get_attribute('data-tab-id')
        self.assertFalse(last_page_id, 'Page id exists.')

    def test_pages_crud(self):
        """
        Scenario: Create/Retrieve/Update/Delete a new page.
        Given that I am on the pages section of a course
        And I add a new page
        Then new page should be added.
        And I edit a page
        Then I should see changes.
        And I delete a page
        Then page should be deleted and no longer be available.
        """
        self.pages_page.visit()

        # Delete any existing pages
        if self.pages_page.get_custom_page_count() > 0:
            self.pages_page.wait_for_the_visibility_of_new_page()
            self.pages_page.delete_all_pages()

        # Get total count of pages currently present.
        page_count = self.pages_page.get_custom_page_count()
        # Add a new page.
        self.pages_page.add_page()
        # Verify that the initial and current page count are not the same.
        self.assert_page_has_been_added(page_count)
        # Now we want to edit the page
        self.pages_page.reload_and_wait_for_page()
        new_page_content = 'New content:{}'.format(uuid4().hex)
        self.pages_page.edit_page(new_page_content, page_count)
        # Assert that updated content is present and successfully saved.
        self.assertIn(
            new_page_content,
            self.pages_page.get_page_content(
                index=page_count
            )
        )
        # And now we delete the page
        self.pages_page.reload_and_wait_for_page()
        # Delete the page.
        self.pages_page.delete_page()
        # Assert that the initial and current page count are the same.
        self.assertEqual(
            page_count, self.pages_page.get_custom_page_count()
        )

        # Verify also that user can click and view See an Example pop up
        # Leaving this at the end in case it leaves the browser
        # with a pop-up showing. We have the configuration such that the
        # browser will exit at the end of every testcase.
        self.pages_page.click_and_verify_see_an_example()


class PagesTestWithLms(WebAppTest):
    """
    Course Pages test where we verify on Lms too
    """
    def setUp(self):
        super(PagesTestWithLms, self).setUp()

        self.course_info = get_course_info()

        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

        self.course_page = CourseInfoPageExtended(
            self.browser, get_course_key(self.course_info)
        )
        self.courseware_page = CoursewarePageExtended(
            self.browser,
            get_course_key(self.course_info)
        )
        self.pages_page = PagesPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        # Login to LMS to avoid authentication issue
        self.course_page.visit()
        self.pages_page.visit()

    def assert_page_is_shown_in_lms(self, page_name):
        """
        Confirms the page is shown in LMS

        Arguments:
            page_name(str): Name of the page to be shown
        """
        self.pages_page.click_view_live_button()
        self.courseware_page.wait_for_page()
        pages_in_tab = self.courseware_page.get_page_names_in_tab()
        self.assertIn(page_name, pages_in_tab)

    def assert_page_is_not_shown_in_lms(self, page_name):
        """
        Confirms the page is not shown in LMS

        Arguments:
            page_name(str): Name of the page not to be shown
        """
        self.pages_page.click_view_live_button()
        self.courseware_page.wait_for_page()
        pages_in_tab = self.courseware_page.get_page_names_in_tab()
        self.assertNotIn(page_name, pages_in_tab)

    @flaky(max_runs=50, min_passes=50)
    def test_hide_and_show_pages(self):
        """
        Verifies that hide/show toggle button is working
        for pages.
        """
        # Reset page state
        self.reset_hide_show_of_page()

        self.pages_page.visit()

        # Click hide/show toggle, assert page is not shown.
        page = self.pages_page.toggle_wiki_page_display()
        self.assertFalse(self.pages_page.toggle_wiki_page_show_value())

        # Assert page is not shown in the LMS.
        self.assert_page_is_not_shown_in_lms(page)

        # Return back to tbe pages page and un-check
        # the toggle to show the page.
        self.pages_page.visit()

        page = self.pages_page.toggle_wiki_page_display()
        self.assertTrue(self.pages_page.toggle_wiki_page_show_value())

        # Assert page is shown in the LMS.
        self.assert_page_is_shown_in_lms(page)

        # Reset page state
        self.reset_hide_show_of_page()

    def reset_hide_show_of_page(self):
        """
        Resets hide/show state of wiki page to default
        """
        self.pages_page.visit()
        if self.pages_page.toggle_wiki_page_show_value() is False:
            self.pages_page.toggle_wiki_page_display()
            self.assertTrue(self.pages_page.toggle_wiki_page_show_value())
