"""
Test uploaded files.
"""
from bok_choy.web_app_test import WebAppTest

from regression.pages.studio.utils import upload_new_file
from regression.pages.studio.login_studio import StudioLogin
from regression.tests.helpers import LoginHelper, get_course_info

from regression.pages.studio.asset_index_studio import AssetIndexPageExtended


class UploadedFileTest(WebAppTest):
    """
    Test uploaded files.
    """
    def setUp(self):
        super(UploadedFileTest, self).setUp()
        self.login_page = StudioLogin(self.browser)
        LoginHelper.login(self.login_page)
        self.course_info = get_course_info()

        self.asset_page = AssetIndexPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.asset_page.visit()
        self.file_names = [
            'README.rst',
            'Image.png'
        ]

    def upload_files(self):
        """
        Upload files
        """
        # Open file upload prompt.
        self.asset_page.open_upload_file_prompt()
        # Upload the files.
        upload_new_file(self.asset_page, self.file_names)
        # Assert that files has been uploaded.
        self.assertEqual(self.file_names, self.asset_page.get_file_names())

    def test_lock_files(self):
        """
        Scenario: Lock the files
        Given that I am on the 'Files & uploads" section of the course.
        And I lock a file.
        Then file should get locked.
        """
        self.upload_files()
        index_of_lock_file = 0
        # Lock the asset present at index passed.
        self.asset_page.lock_asset(index_of_lock_file)
        locked_file_elements = self.asset_page.q(
            css='.assets-table tbody tr .actions-col .lock-checkbox')
        # Assert that file has been locked.
        self.assertTrue(
            locked_file_elements.attrs('checked')[index_of_lock_file])

    def test_sort_files(self):
        """
        Scenario: Lock the files
        Given that I am on the 'Files & uploads" section of the course.
        And I sort the files.
        Then I should see files in sorted order.
        """
        self.upload_files()
        initial_order = self.asset_page.get_file_names()
        # Sort the assets
        self.asset_page.sort_assets()
        initial_order.sort()
        # Assert that assets has been sorted.
        self.assertEqual(initial_order, self.asset_page.get_file_names())

    def test_delete_files(self):
        """
        Scenario: Delete the file
        Given that I am on the 'Files & uploads" section of the course.
        And I delete a file.
        Then file should be deleted and no longer available.
        """
        self.upload_files()
        # Index of files to be deleted.
        file_index_to_delete = [0, 1]
        # Delete the files.
        self.asset_page.delete_file(file_index_to_delete)
        # Assert files has been deleted.
        self.assertNotIn(self.file_names, self.asset_page.get_file_names())
