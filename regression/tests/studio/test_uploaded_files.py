"""
Test uploaded files.
"""
from bok_choy.web_app_test import WebAppTest

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

    def test_files(self):
        """
        Tests on uploaded files.
        Test lock, sort and delete.
        """
        # File names to be uploaded.
        file_names = [
            'README.rst',
            'Image.png'
        ]
        # Open file upload prompt.
        self.asset_page.open_upload_file_prompt()
        # Upload the file.
        self.asset_page.upload_new_file(file_names)
        # Assert that files has been uploaded.
        self.assertEqual(file_names, self.asset_page.get_file_names())
        index_of_lock_file = 0
        # Lock the asset present at index passed.
        self.asset_page.lock_asset(index_of_lock_file)
        locked_file_elements = self.asset_page.q(
            css='.assets-table tbody tr .actions-col .lock-checkbox')
        # Assert that file has been locked.
        self.assertTrue(
            locked_file_elements.attrs('checked')[index_of_lock_file])
        initial_order = self.asset_page.get_file_names()
        # Sort the assets
        self.asset_page.sort_assets()
        initial_order.sort()
        # Assert that assets has been sorted.
        self.assertEqual(initial_order, self.asset_page.get_file_names())
        # Index of files to be deleted.
        file_index_to_delete = [0, 1]
        # Delete the files.
        self.asset_page.delete_file(file_index_to_delete)
        # Assert files has been deleted.
        self.assertNotIn(file_names, self.asset_page.get_file_names())
