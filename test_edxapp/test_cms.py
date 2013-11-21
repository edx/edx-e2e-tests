"""
E2E tests for Studio.
"""

from e2e_framework.web_app_test import WebAppTest
from pages.cms.login import LoginPage
from pages.cms.howitworks import HowitworksPage
from pages.cms.signup import SignupPage


class LoggedOutTest(WebAppTest):
    """
    Smoke test for pages in Studio
    that are visible when logged out.
    """

    @property
    def page_object_classes(self):
        return [
            LoginPage, HowitworksPage, SignupPage
        ]

    def test_page_existence(self):
        """
        Make sure that all the pages are accessible.
        Rather than fire up the browser just to check each url,
        do them all sequentially in this testcase.
        """
        pages = [
            'login', 'howitworks', 'signup'
        ]

        for page in pages:
            self.ui.visit('cms.{0}'.format(page))
