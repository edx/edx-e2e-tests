"""
Test help link on video upload page.
"""
from __future__ import absolute_import

from unittest import skipIf

from bok_choy.web_app_test import WebAppTest

from edxapp_acceptance.tests.helpers import assert_nav_help_link
from regression.pages.studio import STUDIO_BASE_URL
from regression.pages.studio.video_upload_studio import VideoUploadPage
from regression.tests.helpers.api_clients import StudioLoginApi
from regression.tests.helpers.utils import get_course_info


class TestVideoUploadHelp(WebAppTest):
    """
    Test help link on video upload page.
    """
    def setUp(self):
        """
        Initialize the page object
        """
        super(TestVideoUploadHelp, self).setUp()

        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)

        self.course_info = get_course_info()
        self.video_upload_page = VideoUploadPage(
            self.browser,
            self.course_info['org'],
            self.course_info['number'],
            self.course_info['run'])

        self.video_upload_page.visit()

    @skipIf(
        STUDIO_BASE_URL.startswith('edx.devstack'),
        "No video upload pipeline on Docker Devstack"
    )
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
                        'en/latest/video/index.html'
        # Assert that help link is correct.
        assert_nav_help_link(
            test=self,
            page=self.video_upload_page,
            href=expected_href
        )
