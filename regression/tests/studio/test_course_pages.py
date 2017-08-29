"""
Course pages test
"""
from uuid import uuid4

from bok_choy.web_app_test import WebAppTest

from regression.tests.helpers.api_clients import StudioSessionApi
from regression.tests.helpers.utils import get_course_info
from regression.pages.studio.pages_page_studio import PagesPageExtended


class CoursePagesTest(WebAppTest):
    """
    Course Pages test
    """
    def setUp(self):
        super(CoursePagesTest, self).setUp()
        self.course_info = get_course_info()

        login_api = StudioSessionApi()
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

