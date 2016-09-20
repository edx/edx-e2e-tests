"""
Test textbook page
"""

from bok_choy.web_app_test import WebAppTest

from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.studio_textbooks import TextbookPageExtended
from regression.tests.helpers.helpers import LoginHelper, get_course_info


class TextbookTest(WebAppTest):
    """
    Test textbooks.
    """
    def setUp(self):
        super(TextbookTest, self).setUp()
        self.login_page = StudioLogin(self.browser)
        LoginHelper.login(self.login_page)
        self.course_info = get_course_info()

        self.textbook_page = TextbookPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        self.textbook_page.visit()

    def test_textbook_edit(self):
        """
        Verifies that textbook can be edited
        """
        # Pre-req
        self.textbook_page.open_add_textbook_form()
        self.textbook_page.set_input_field_value(
            '.edit-textbook #textbook-name-input', 'book_1')
        self.textbook_page.set_input_field_value(
            '.edit-textbook #chapter1-name', 'chap_1')
        self.textbook_page.upload_textbook('test_pdf.pdf')
        self.textbook_page.click_textbook_submit_button()
        # Edit
        self.textbook_page.click_edit_button()
        self.textbook_page.set_input_field_value(
            '.edit-textbook #textbook-name-input', 'edit')
        self.textbook_page.set_input_field_value(
            '.edit-textbook #chapter1-name', 'edit')
        self.textbook_page.click_textbook_submit_button()
        self.assertEquals(self.textbook_page.get_element_text(
            '.textbook-title'), 'book_1edit')
        # Delete
        self.textbook_page.click_delete_button()
        message = self.textbook_page.get_element_text(
            '.wrapper-content .no-textbook-content')
        self.assertIn("You haven't added any textbooks", message)

    def test_textbook_delete(self):
        """
        Verifies that the added textbook can be deleted
        """
        # Pre-req
        self.textbook_page.open_add_textbook_form()
        self.textbook_page.set_input_field_value(
            '.edit-textbook #textbook-name-input', 'book_1')
        self.textbook_page.set_input_field_value(
            '.edit-textbook #chapter1-name', 'chap_1')
        self.textbook_page.upload_textbook('test_pdf.pdf')
        self.textbook_page.click_textbook_submit_button()
        # Delete
        self.textbook_page.click_delete_button()
        message = self.textbook_page.get_element_text(
            '.wrapper-content .no-textbook-content')
        self.assertIn("You haven't added any textbooks", message)
