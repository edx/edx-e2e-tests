"""
Test help link on video upload page.
"""
from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.tests.helpers import assert_nav_help_link

from regression.pages.studio.video_upload_studio import VideoUploadPage
from regression.pages.studio.login_studio import StudioLogin
from regression.tests.helpers import LoginHelper, get_course_info


class TestVideoUploadHelp(WebAppTest):
    """
    Test help link on video upload page.
    """
    def setUp(self):
        """
        Initialize the page object
        """
        super(TestVideoUploadHelp, self).setUp()

        self.login_page = StudioLogin(self.browser)
        self.course_info = get_course_info()
        self.video_upload_page = VideoUploadPage(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        LoginHelper.login(self.login_page)
        self.video_upload_page.visit()

    def test_video_upload_nav_help(self):
        """
        Scenario: Help link in navigation bar is working on
        'Upload video' page.
        Given that I am on the 'Upload video' page.
        And I want help about the it.
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'video/video_uploads.html'
        """
        # The url we want to see in anchor help element.
        expected_href = 'https://edx.readthedocs.io/projects/edx-partner-course-staff/' \
                        'en/latest/video/video_uploads.html'
        # Assert that help link is correct.
        assert_nav_help_link(
            test=self,
            page=self.video_upload_page,
            href=expected_href
        )
