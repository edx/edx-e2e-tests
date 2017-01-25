"""
Test uploaded files, aka Assets
"""

from regression.pages.studio.asset_index_studio import AssetIndexPageExtended
from regression.pages.studio.utils import upload_new_file
from regression.tests.helpers import StudioLoginApi, get_course_info
from regression.tests.studio.studio_base_test import BaseTestClassNoCleanup


class TestAssetCrud(BaseTestClassNoCleanup):
    """ Test create/read/update/delete of course assets"""
    def test_asset_crud(self):
        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)
        course_info = get_course_info()

        asset_page = AssetIndexPageExtended(
            self.browser,
            course_info['org'],
            course_info['number'],
            course_info['run']
        )
        asset_page.visit()
        file_names = ['README.rst', 'test_pdf.pdf']

        # The course should start with no assets uploaded.
        # There is a bit of Uncertainty Principle here, as we are
        # using the feature itself to set up the course context.
        # TODO: this should be replaced when we have a better
        # mechanism for setting up courses for testing.
        asset_page.delete_all_assets()  # Put the course in a known state
        # There should be no uploaded assets
        self.assertEqual(asset_page.asset_files_count, 0)

        # Upload the files
        asset_page.open_upload_file_prompt()
        upload_new_file(asset_page, file_names)
        # Assert that the files have been uploaded.
        self.assertEqual(file_names, asset_page.asset_files_names)

        # Verify that a file can be locked
        asset_page.set_asset_lock()
        # Get the list of locked assets, there should be one
        locked_assets = asset_page.asset_locks(locked_only=True)
        self.assertEqual(len(locked_assets), 1)

        # Confirm that there are 2 assets, with the first
        # locked and the second unlocked.
        all_assets = asset_page.asset_locks(locked_only=False)
        self.assertEqual(len(all_assets), 2)
        self.assertTrue(all_assets[0].get_attribute('checked'))
        self.assertIsNone(all_assets[1].get_attribute('checked'))

        # Verify that the files can be deleted
        for name in asset_page.asset_files_names:
            asset_page.delete_first_asset()
            # Assert files have been deleted.
            self.assertNotIn(name, asset_page.asset_files_names)

        # There should now be no uploaded assets
        self.assertEqual(asset_page.asset_files_count, 0)
