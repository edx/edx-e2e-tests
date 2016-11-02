"""
Course pages test
"""
from uuid import uuid4
from bok_choy.web_app_test import WebAppTest

from edxapp_acceptance.pages.lms.courseware import CoursewarePage
from regression.pages.studio.login_studio import StudioLogin
from regression.tests.helpers import LoginHelper, get_course_info
from regression.pages.studio.pages_page_studio import PagesPageExtended
from regression.pages.lms.login_lms import LmsLogin


class CoursePagesTest(WebAppTest):
    """
    Course Pages test
    """
    def setUp(self):
        super(CoursePagesTest, self).setUp()
        self.course_info = get_course_info()
        self.login_page = StudioLogin(self.browser)
        LoginHelper.login(self.login_page)
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
        current_page_count = self.pages_page.get_page_count()
        self.assertGreater(
            current_page_count, initial_page_count
        )
        last_page_id = self.pages_page.q(
            css='.component.course-tab.is-movable'
        ).results[current_page_count - 1].get_attribute('data-tab-id')
        self.assertFalse(last_page_id, 'Page id exists.')

    def test_add_page(self):
        """
        Scenario: Add a new page.
        Given that I am on the pages section of a course
        And I add a new page
        Then new page should be added.
        """
        self.pages_page.visit()
        # Get total count of pages currently present.
        initial_page_count = self.pages_page.get_page_count()
        # Add a new page.
        self.pages_page.add_page()
        # Verify that the initial and current page count are not the same.
        self.assert_page_has_been_added(initial_page_count)

    def test_edit_page(self):
        """
        Scenario: Edit a page.
        Given that I am on the pages section of a course
        And I edit a page
        Then I should see changes.
        """
        self.pages_page.visit()
        page_count = self.pages_page.get_page_count()
        # Add a new page.
        self.pages_page.add_page()
        # Verify that the initial and current page count are not the same.
        self.assert_page_has_been_added(page_count)
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

    def test_delete_page(self):
        """
        Scenario: Delete a new page.
        Given that I am on the pages section of a course
        And I delete a page
        Then page should be deleted and no longer be available.
        """
        self.pages_page.visit()
        page_count = self.pages_page.get_page_count()
        # Add a new page.
        self.pages_page.add_page()
        # Verify that the initial and current page count are not the same.
        self.assert_page_has_been_added(page_count)
        self.pages_page.reload_and_wait_for_page()
        # Delete the page.
        self.pages_page.delete_page()
        # Assert that the initial and current page count are the same.
        self.assertEqual(
            page_count, self.pages_page.get_page_count()
        )

    def test_see_an_example_popup(self):
        """
        Verifies that user can click and view See an Example pop up
        """
        self.pages_page.visit()
        self.pages_page.click_and_verify_see_an_example()


class PagesTestWithLms(WebAppTest):
    """
    Course Pages test where we verify on Lms too
    """
    def setUp(self):
        super(PagesTestWithLms, self).setUp()
        self.course_info = get_course_info()
        # Login to Lms first to avoid authentication
        self.login_page = LmsLogin(self.browser)
        LoginHelper.login(self.login_page)

        self.studio_login_page = StudioLogin(self.browser)
        LoginHelper.login(self.studio_login_page)
        self.pages_page = PagesPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.pages_page.visit()

    def test_view_live_pages(self):
        """
        Verifies that user can View live course from pages page
        """
        self.pages_page.click_view_live_button()
        courseware_page = CoursewarePage(
            self.browser, get_course_info())
        courseware_page.wait_for_page()
