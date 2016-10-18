"""
Test course update
"""
from uuid import uuid4

from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.course_info_studio import (
    CourseUpdatesPageExtended
)
from regression.tests.studio.studio_base_test import StudioBaseTestClass
from regression.tests.helpers import LoginHelper, get_course_info


class CourseUpdateTest(StudioBaseTestClass):
    """
    Test course update.
    """
    def setUp(self):
        super(CourseUpdateTest, self).setUp()
        self.login_page = StudioLogin(self.browser)
        LoginHelper.login(self.login_page)
        self.course_info = get_course_info()

        self.course_update_page = CourseUpdatesPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.course_update_page.visit()
        self.course_update_content_selector = '#course-update-list li' \
                                              ' .post-preview .update-contents'
        self.course_update_text = 'New update:{}'.format(uuid4().hex)

    def create_course_update(self):
        """
        Create course update and verify
        """
        self.course_update_page.open_new_update_form()
        self.course_update_page.write_update_and_save(self.course_update_text)
        # Assert course update has been created successfully.
        self.assertEqual(
            self.course_update_page.q(
                css=self.course_update_content_selector)[0].text,
            self.course_update_text
        )

    def test_create_course_update(self):
        """
        Verifies creation of course update
        """
        # Create course update
        self.create_course_update()

    def test_edit_course_update(self):
        """
        Verify editing course update
        """
        # Create course update
        self.create_course_update()

        # Edit course update
        course_update_edit_text = 'Edited update:{}'.format(uuid4().hex)
        # Edit the course update and save.
        self.course_update_page.edit_course_update(course_update_edit_text)
        # Verify that the edit has been saved correctly and is visible.
        self.assertEqual(
            self.course_update_page.q(
                css=self.course_update_content_selector)[0].text,
            course_update_edit_text
        )

    def test_delete_course_update(self):
        """
        Verify deletion of course update
        """
        # Create course update
        self.create_course_update()
        # Delete course update
        self.course_update_page.delete_course_update()
        # If there are no course updates present anymore
        #  then we assume that deletion was successful.
        #  If present then make sure the contents don't match.
        if self.course_update_page.q(
                css=self.course_update_content_selector).present:
            self.assertNotEqual(
                self.course_update_page.q(
                    css=self.course_update_content_selector)[0].text,
                self.course_update_text
            )


class CourseHandoutTest(StudioBaseTestClass):
    """
    Test course handout
    """
    def setUp(self):
        super(CourseHandoutTest, self).setUp()
        self.login_page = StudioLogin(self.browser)
        LoginHelper.login(self.login_page)
        self.course_info = get_course_info()

        self.course_update_page = CourseUpdatesPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.course_update_page.visit()

    def test_edit_course_handout(self):
        """
        Verifies that user can edit course handout
        """
        course_handout_content = 'New handout content:{}'.format(uuid4().hex)
        # Edit course handout
        self.course_update_page.edit_course_handout(course_handout_content)
        # Verify that the edit has been saved correctly and is visible.
        self.assertEqual(
            self.course_update_page.q(css='.handouts-content')[0].text,
            course_handout_content
        )
        # Discard the update.
        self.course_update_page.edit_course_handout("")
        # Verify that the edit has been saved correctly and is visible.
        self.assertEqual(
            self.course_update_page.q(css='.handouts-content')[0].text,
            ""
        )
