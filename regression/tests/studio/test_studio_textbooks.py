"""
Test textbook page
"""
from uuid import uuid4

from regression.tests.studio.studio_base_test import StudioBaseTestClass

from regression.pages.studio.studio_textbooks import TextbookPageExtended
from regression.tests.helpers.api_clients import (
    StudioLoginApi, LmsLoginApi
)
from regression.tests.helpers.utils import get_course_info
from regression.pages.lms.lms_textbook import TextbookPage


class TextbookTest(StudioBaseTestClass):
    """
    Test textbooks.
    """
    def setUp(self):
        super(TextbookTest, self).setUp()

        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

        self.lms_textbook = TextbookPage(self.browser)
        self.course_info = get_course_info()

        self.textbook_page = TextbookPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        self.textbook_page.visit()

    def test_textbook_crud(self):
        """
        Verifies that user can add, verify, edit and delete textbook
        """
        # Add textbook
        textbook_name = 'book_{}'.format(uuid4().hex)
        chapter_name = 'chap_1'
        self.textbook_page.open_add_textbook_form()
        self.textbook_page.set_input_field_value(
            '.edit-textbook #textbook-name-input', textbook_name
        )
        self.textbook_page.set_input_field_value(
            '.edit-textbook #chapter1-name', chapter_name
        )
        self.textbook_page.upload_textbook('test_pdf.pdf')

        # Verify the added textbook on LMS
        self.textbook_page.click_textbook_submit_button()
        self.textbook_page.click_view_live_textbook()
        self.lms_textbook.wait_for_page()
        self.assertIn(
            chapter_name, self.lms_textbook.q(css='.chapter').text
        )

        # Navigate back to studio
        self.textbook_page.visit()

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
            textbook_name + 'edit'
        )

        # Delete the textbook
        self.textbook_page.click_delete_button()

        if self.textbook_page.get_textbook_count() > 0:
            self.assertNotIn(
                textbook_name, self.textbook_page.get_textbook_names()
            )
