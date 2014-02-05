"""
Acceptance tests for Studio.
"""
from bok_choy.web_app_test import WebAppTest

from edxapp_pages.studio.asset_index import AssetIndexPage
from edxapp_pages.studio.auto_auth import AutoAuthPage
from edxapp_pages.studio.checklists import ChecklistsPage
from edxapp_pages.studio.course_import import ImportPage
from edxapp_pages.studio.course_info import CourseUpdatesPage
from edxapp_pages.studio.edit_tabs import StaticPagesPage
from edxapp_pages.studio.export import ExportPage
from edxapp_pages.studio.howitworks import HowitworksPage
from edxapp_pages.studio.index import DashboardPage
from edxapp_pages.studio.login import LoginPage
from edxapp_pages.studio.manage_users import CourseTeamPage
from edxapp_pages.studio.overview import CourseOutlinePage
from edxapp_pages.studio.settings import SettingsPage
from edxapp_pages.studio.settings_advanced import AdvancedSettingsPage
from edxapp_pages.studio.settings_graders import GradingPage
from edxapp_pages.studio.signup import SignupPage
from edxapp_pages.studio.textbooks import TextbooksPage

from ..helpers import visit_all


class PagesTest(WebAppTest):
    """
    Smoke test that we can visit pages in Studio.
    """

    # We use the global staff user to log in, because we know they will have access
    # to Studio.  This is not ideal, and longer term we should install and test with
    # instructor/course-staff users instead.
    STUDIO_USER = "staff@example.com"
    STUDIO_PASSWORD = "edx"

    DEMO_COURSE_INFO = ('edX', 'Open_DemoX', 'edx_demo_course')

    def test_logged_out_pages(self):
        visit_all([
            clz(self.browser) for clz in [LoginPage, HowitworksPage, SignupPage]
        ])

    def test_logged_in_pages(self):

        # Log in to Studio
        login_page = LoginPage(self.browser)
        login_page.visit()
        login_page.login(self.STUDIO_USER, self.STUDIO_PASSWORD)

        # Check that we can get to the dashboard
        DashboardPage(self.browser).wait_for_page()

        # Check that we can get to course editing pages
        visit_all([
            clz(self.browser, *self.DEMO_COURSE_INFO) for clz in
            [AssetIndexPage, ChecklistsPage, ImportPage, CourseUpdatesPage,
            StaticPagesPage, ExportPage, CourseTeamPage, CourseOutlinePage, SettingsPage,
            AdvancedSettingsPage, GradingPage, TextbooksPage]])
