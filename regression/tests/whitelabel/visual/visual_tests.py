"""
Visual Tests
"""
from bok_choy.web_app_test import WebAppTest
from regression.pages.whitelabel.const import (
    VISUAL_USER_EMAIL,
    PASSWORD,
    PROF_COURSE_ID
)
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.dashboard_page import DashboardPage
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.logistration_page import (
    LoginPage,
    RegistrationPage
)
from regression.pages.whitelabel.static_pages import (
    AboutPage,
    FaqPage,
    ContactUsPage,
    TosPage,
    PrivacyPolicyPage,
    HonorCodePage
)
from regression.pages.whitelabel.profile_page import ProfilePage


class VisualTest(WebAppTest):
    """
    Visual Tests Class
    """

    # Cleanup dat on success
    cleanup_on_success = True

    def setUp(self):
        """
        Initialize all page objects
        """
        super(VisualTest, self).setUp()
        self.set_viewport_size(1024, 768)
        self.css_locator_header = '.header-main'
        self.css_locator_banner = '.hero-main'
        self.css_locator_login_reg_container = '#login-and-registration-' \
                                               'container'
        self.css_locator_about_section = '.about-container'
        self.css_locator_footer = '.footer-main'
        self.css_locator_static_pages_banner = '.page-heading>h1'
        self.css_locator_static_pages_message = '.static-content'
        self.platform_name = "MIT"

    def test_00_verify_home_page(self):
        """
        Scenario: To verify that all elements on home page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('Home')
        home = HomePage(self.browser).visit()
        self.assertTrue(home.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(home.q(css=self.css_locator_banner).visible)
        self.assertScreenshot(self.css_locator_banner, page + 'Banner')
        self.assertTrue(home.q(css=self.css_locator_about_section).visible)
        self.assertScreenshot(
            self.css_locator_about_section, page + 'About_Section')
        self.assertTrue(home.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_01_verify_login_page(self):
        """
        Scenario: To verify that all elements on login page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('Login')
        login = LoginPage(self.browser).visit()
        self.assertTrue(login.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(login.q(
            css=self.css_locator_login_reg_container).visible)
        self.assertScreenshot(
            self.css_locator_login_reg_container, page + 'Container')

    def test_02_verify_registration_page(self):
        """
        Scenario: To verify that all elements on registration page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('Registration')
        register = RegistrationPage(self.browser).visit()
        self.assertTrue(register.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(register.q(
            css=self.css_locator_login_reg_container).visible)
        self.assertScreenshot(
            self.css_locator_login_reg_container, page + 'Container')

    def test_03_verify_about_page(self):
        """
        Scenario: To verify that all elements on about page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('About')
        about = AboutPage(self.browser).visit()
        self.assertTrue(about.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(about.q(
            css=self.css_locator_static_pages_banner).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_banner, page + 'Banner')
        self.assertTrue(about.q(
            css=self.css_locator_static_pages_message).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_message, page + 'Message')
        self.assertTrue(about.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_05_verify_faq_page(self):
        """
        Scenario: To verify that all elements on faq page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('FAQ')
        faq = FaqPage(self.browser).visit()
        self.assertTrue(faq.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(faq.q(
            css=self.css_locator_static_pages_banner).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_banner, page + 'Banner')
        self.assertTrue(faq.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_06_verify_contact_page(self):
        """
        Scenario: To verify that all elements on contact page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('Contact')
        contact = ContactUsPage(self.browser).visit()
        self.assertTrue(contact.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(contact.q(
            css=self.css_locator_static_pages_banner).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_banner, page + 'Banner')
        self.assertTrue(contact.q(
            css=self.css_locator_static_pages_message).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_message, page + 'Message')
        self.assertTrue(contact.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_07_verify_tos_page(self):
        """
        Scenario: To verify that all elements on Terms of Services page are
        rendered correctly
        """
        page = self.page_name_prefix_builder('TOS')
        tos = TosPage(self.browser).visit()
        self.assertTrue(tos.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(tos.q(
            css=self.css_locator_static_pages_banner).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_banner, page + 'Banner')
        self.assertTrue(tos.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_08_verify_privacy_policy_page(self):
        """
        Scenario: To verify that all elements on Privacy Policy page are
        rendered correctly
        """
        page = self.page_name_prefix_builder('Privacy_Policy')
        privacy_policy = PrivacyPolicyPage(self.browser).visit()
        self.assertTrue(privacy_policy.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(privacy_policy.q(
            css=self.css_locator_static_pages_banner).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_banner, page + 'Banner')
        self.assertTrue(privacy_policy.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_09_verify_honor_code_page(self):
        """
        Scenario: To verify that all elements on contact page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('Honor_Code')
        honor_code = HonorCodePage(self.browser).visit()
        self.assertTrue(honor_code.q(css=self.css_locator_header).visible)
        self.assertScreenshot(
            self.css_locator_header, page + 'Header')
        self.assertTrue(honor_code.q(
            css=self.css_locator_static_pages_banner).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_banner, page + 'Banner')
        self.assertTrue(honor_code.q(
            css=self.css_locator_static_pages_message).visible)
        self.assertScreenshot(
            self.css_locator_static_pages_message, page + 'Message')
        self.assertTrue(honor_code.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_10_verify_profile_page(self):
        """
        Scenario: To verify that all elements on profile page are rendered
        correctly
        """
        page = self.page_name_prefix_builder('Profile')
        login = LoginPage(self.browser)
        dashboard = DashboardPage(self.browser)
        css_locator_privacy = '.wrapper-profile-field-account-privacy'
        css_locator_setting_container = \
            '.wrapper-profile-sections.account-settings-container'
        login.visit()
        # Login to application
        login.authenticate_user(VISUAL_USER_EMAIL, PASSWORD, dashboard)
        # Open the profile page
        dashboard.go_to_profile_page()
        profile = ProfilePage(self.browser)
        # Take and compare screen shots
        self.assertTrue(profile.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(profile.q(css=css_locator_privacy).visible)
        self.assertScreenshot(css_locator_privacy, page + 'Privacy')
        self.assertTrue(profile.q(css=css_locator_setting_container).visible)
        self.assertScreenshot(css_locator_setting_container, page + 'Settings')
        self.assertTrue(profile.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def test_11_verify_course_about_page(self):
        """
        Scenario: To verify that all elements on course about page are
        rendered correctly
        """
        page = self.page_name_prefix_builder('Course')
        course_about = CourseAboutPage(
            self.browser, PROF_COURSE_ID).visit()
        css_locator_course_banner = '.hero-image'
        css_locator_course_detail = '.course-detail.light-bg'
        css_locator_course_info = '.course-info>.grid-manual.grid-container'
        # Take and compare screen shots
        self.assertTrue(course_about.q(css=self.css_locator_header).visible)
        self.assertScreenshot(self.css_locator_header, page + 'Header')
        self.assertTrue(course_about.q(css=css_locator_course_banner).visible)
        self.assertScreenshot(css_locator_course_banner, page + 'Banner')
        self.assertTrue(course_about.q(
            css=self.css_locator_about_section).visible)
        self.assertScreenshot(css_locator_course_detail, page + 'Detail')
        self.assertTrue(course_about.q(css=css_locator_course_info).visible)
        self.assertScreenshot(css_locator_course_info, page + 'Info')
        self.assertTrue(course_about.q(
            css=self.css_locator_about_section).visible)
        self.assertScreenshot(
            self.css_locator_about_section, page + 'About_Section')
        self.assertTrue(course_about.q(css=self.css_locator_footer).visible)
        self.assertScreenshot(self.css_locator_footer, page + 'Footer')

    def page_name_prefix_builder(self, page_name):
        """
        Build page name prefix for naming images
        :param page_name:
        :return: Complete Page name prefix
        """
        return self.platform_name + '_' + page_name + '_'
