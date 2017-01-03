"""
Test uploaded files.
"""
import os
from shutil import copyfile
from regression.tests.studio.studio_base_test import StudioBaseTestClass
from regression.pages.studio.utils import upload_new_file
from regression.tests.helpers import get_course_info

from regression.pages.studio.asset_index_studio import AssetIndexPageExtended
from regression.pages import UPLOAD_FILE_DIR


class UploadedFileTest(StudioBaseTestClass):
    """
    Test uploaded files.
    """
    def setUp(self):
        super(UploadedFileTest, self).setUp()
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
            'test_pdf.pdf'
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
        Scenario: Sort the files
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
        file_names = self.asset_page.get_file_names()
        for name in file_names:
            self.asset_page.click_delete_file()
            # Assert files have been deleted.
            self.assertNotIn(name, self.asset_page.get_file_names())


class UploadedFilePaginationTest(StudioBaseTestClass):
    """
    Test uploaded files.
    """
    def setUp(self):
        super(UploadedFilePaginationTest, self).setUp()
        self.course_info = get_course_info()

        self.asset_page = AssetIndexPageExtended(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run']
        )
        self.asset_page.visit()

    def test_pagination(self):
        """
        Verifies that user can successfully navigate between multiple pages
        """
        file_name = '{}.png'
        file_names = ['1.png']
        for num in range(2, 52):
            file_names.append(file_name.format(num))
            copyfile(
                UPLOAD_FILE_DIR + '/' + '1.png',
                UPLOAD_FILE_DIR + '/' + file_name.format(num)
            )

        # Open file upload prompt.
        self.asset_page.open_upload_file_prompt()
        # Upload the files.
        upload_new_file(self.asset_page, file_names)
        # Assert that pages are now 2 in total.
        self.assertEqual('1', self.asset_page.get_page_count())
        self.asset_page.click_next_page_link()
        # Assert that pages are now 2 in total.
        self.assertEqual('2', self.asset_page.get_page_count())

        file_names.pop(0)
        # Remove files from directory
        for file_name in file_names:
            os.remove(UPLOAD_FILE_DIR + '/' + file_name)
