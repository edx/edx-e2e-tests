"""
Test studio grading
"""
from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.grading_studio import GradingPageExtended

from regression.tests.helpers import LoginHelper, get_course_info


class StudioGradingTest(WebAppTest):
    """
    Test studio grading
    """
    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioGradingTest, self).setUp()
        self.login_page = StudioLogin(self.browser)
        self.course_info = get_course_info()
        self.grading_page = GradingPageExtended(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

        LoginHelper.login(self.login_page)

        self.grading_page.visit()

    def test_grade_range(self):
        """
        Verifies default, addition and deletion of grade range
        """
        # Default
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Addition
        self.grading_page.click_new_grade_button()
        self.assertEquals(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Verify that after refreshing, changes remain intact
        self.browser.refresh()
        self.assertEquals(self.grading_page.letter_grade('.letter-grade'), 'A')
        # Deletion
        self.grading_page.click_remove_grade()
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
        # Verify that after refreshing, changes remain intact
        self.browser.refresh()
        self.assertEquals(
            self.grading_page.letter_grade('.letter-grade'), 'Pass')
