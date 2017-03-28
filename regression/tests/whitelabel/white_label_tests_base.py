"""
Base class for white label tests
"""
from bok_choy.web_app_test import WebAppTest

from regression.pages.whitelabel.dashboard_page import DashboardPageExtended
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.registration_page import RegisterPageExtended
from regression.pages.whitelabel.login_page import LoginPage


class WhiteLabelTestsBaseClass(WebAppTest):
    """
    Mixin for User Authentication
    """
    def setUp(self):
        """
        Setup for all common features
        """
        super(WhiteLabelTestsBaseClass, self).setUp()
        # Initialize all page objects
        self.home_page = HomePage(self.browser)
        self.dashboard_page = DashboardPageExtended(self.browser)
        self.login_page = LoginPage(self.browser)
        self.registration_page = RegisterPageExtended(self.browser)
