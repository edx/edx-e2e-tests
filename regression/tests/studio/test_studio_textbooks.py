"""
Test textbook page
"""
from uuid import uuid4

from regression.tests.studio.studio_base_test import StudioBaseTestClass

from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.studio_textbooks import TextbookPageExtended
from regression.tests.helpers import LoginHelper, get_course_info
from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.lms_textbook import TextbookPage


class TextbookTest(StudioBaseTestClass):
    """
    Test textbooks.
    """
    def setUp(self):
        super(TextbookTest, self).setUp()
        # Login to Lms first to avoid authentication
        self.lms_login_page = LmsLogin(self.browser)
        LoginHelper.login(self.lms_login_page)

        self.login_page = StudioLogin(self.browser)
        self.lms_textbook = TextbookPage(self.browser)
        LoginHelper.login(self.login_page)
        self.course_info = get_course_info()

        self.textbook_page = TextbookPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        self.textbook_page.visit()
        self.textbook_name = 'book_{}'.format(uuid4().hex)
        self.chapter_name = 'chap_1'
        # Add textbook
        self.add_textbook()

    def add_textbook(self):
        """
        Add textbook
        """
        self.textbook_page.open_add_textbook_form()
        self.textbook_page.set_input_field_value(
            '.edit-textbook #textbook-name-input', self.textbook_name
        )
        self.textbook_page.set_input_field_value(
            '.edit-textbook #chapter1-name', self.chapter_name
        )
        self.textbook_page.upload_textbook('test_pdf.pdf')
        self.textbook_page.click_textbook_submit_button()

    def test_textbook_verify_on_lms(self):
        """
        Verifies that user can add and visit textbook on LMS
        """
        self.add_textbook()
        self.textbook_page.click_view_live_textbook()
        self.lms_textbook.wait_for_page()
        self.assertIn(
            self.chapter_name, self.lms_textbook.q(css='.chapter').text
        )

    def test_textbook_edit(self):
        """
        Verifies that textbook can be edited
        """
        # Edit the textbook
        self.textbook_page.click_edit_button()
        self.textbook_page.set_input_field_value(
            '.edit-textbook #textbook-name-input', 'edit'
        )
        self.textbook_page.set_input_field_value(
            '.edit-textbook #chapter1-name', 'edit'
        )
        self.textbook_page.click_textbook_submit_button()

        self.assertEquals(
            self.textbook_page.get_textbook_names()[-1],
            self.textbook_name + 'edit'
        )

    def test_textbook_delete(self):
        """
        Verifies that the added textbook can be deleted
        """
        # Delete
        self.textbook_page.click_delete_button()

        if self.textbook_page.get_textbook_count() > 0:
            self.assertNotIn(
                self.textbook_name, self.textbook_page.get_textbook_names()
            )
