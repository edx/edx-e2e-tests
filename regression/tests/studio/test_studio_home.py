"""
End to end tests for Studio Home page
"""


import os
from unittest import skipIf
from unittest import skip

from bok_choy.web_app_test import WebAppTest

from edxapp_acceptance.pages.studio.overview import CourseOutlinePage
from regression.pages.studio import STUDIO_BASE_URL, STUDIO_STAGE_BASE_URL
from regression.pages.studio.privacy_policy import PrivacyPolicy
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.studio.terms_of_service import TermsOfService
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_display_name, get_course_info


class StudioHomeTest(WebAppTest):
    """
    Test for navigating to the Studio Home page
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super().setUp()

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePage(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

    @skip("BOM-2460: Test is failing on Ubuntu 20.04.")
    def test_studio_course_select(self):
        """
        Verifies that user can select a course and navigate to its course
        outline page
        """
        self.studio_home_page.visit()
        self.studio_home_page.select_course(get_course_display_name())
        self.studio_course_outline.wait_for_page()


class StudioFooterTest(WebAppTest):
    """
    Tests for Studio Footer
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super().setUp()

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

        self.terms_of_service = TermsOfService(self.browser)
        self.privacy_policy = PrivacyPolicy(self.browser)
        self.studio_home_page = DashboardPageExtended(self.browser)
        self.course_info = get_course_info()
        self.studio_course_outline = CourseOutlinePage(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

        self.studio_home_page.visit()

    @skip("BOM-2460: Test is failing on Ubuntu 20.04.")
    def test_studio_footer_links(self):
        """
        Verifies that user can click and navigate to studio footer links
        Terms of Service
        Privacy Policy
        """

        self.studio_home_page.click_terms_of_service()
        self.terms_of_service.wait_for_page()
        self.studio_home_page.visit()
        self.studio_home_page.click_privacy_policy()
        self.privacy_policy.wait_for_page()
