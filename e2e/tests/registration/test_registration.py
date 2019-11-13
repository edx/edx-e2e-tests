import unittest

from e2e.main.pages.registration_page import RegistrationPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.tests.main_class import MainClass
from e2e.main.pages.login_page import LoginPage

class TestRegistration(MainClass):

    def setUp(self):
        super(TestRegistration, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.registration_page = RegistrationPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        # suite working 3m 44s

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_01_registration_with_correct_dataes(self):
        '''Checking registration with correct dataes'''
        self.logger.do_test_name("Checking registration with correct dataes")
        email = self.registration_page.getEmail()
        username = self.registration_page.getUsername()
        self.registration_page.registration(email, variables.FULL_NAME, username, variables.LOGIN_PASSWORD, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(email)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_02_registration_without_email(self):
        '''Checking registration without email'''
        self.logger.do_test_name("Checking registration without email")
        username = self.registration_page.getUsername()
        self.registration_page.registration(variables.EMPTY, variables.FULL_NAME, username, variables.LOGIN_PASSWORD, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_EMPTY_EMAIL_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(variables.EMPTY, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.FULL_NAME, self.registration_page.getValueFullName())
        self.config.do_assert_true(username, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.LOGIN_PASSWORD, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_03_registration_without_full_name(self):
        '''Checking registration without full name'''
        self.logger.do_test_name("Checking registration without full name")
        email = self.registration_page.getEmail()
        username = self.registration_page.getUsername()
        self.registration_page.registration(email, variables.EMPTY, username, variables.LOGIN_PASSWORD, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_EMPTY_FULL_NAME_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(email, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.EMPTY, self.registration_page.getValueFullName())
        self.config.do_assert_true(username, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.LOGIN_PASSWORD, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_04_registration_without_username(self):
        '''Checking registration without username'''
        self.logger.do_test_name("Checking registration without username")
        email = self.registration_page.getEmail()
        self.registration_page.registration(email, variables.FULL_NAME, variables.EMPTY, variables.LOGIN_PASSWORD, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_EMPTY_USERNAME_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(email, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.FULL_NAME, self.registration_page.getValueFullName())
        self.config.do_assert_true(variables.EMPTY, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.LOGIN_PASSWORD, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_05_registration_without_password(self):
        '''Checking registration without password'''
        self.logger.do_test_name("Checking registration without password")
        email = self.registration_page.getEmail()
        username = self.registration_page.getUsername()
        self.registration_page.registration(email, variables.FULL_NAME, username, variables.EMPTY, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_EMPTY_PASSWORD_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(email, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.FULL_NAME, self.registration_page.getValueFullName())
        self.config.do_assert_true(username, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.EMPTY, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_06_registration_without_agree(self):
        '''Checking registration without agree'''
        self.logger.do_test_name("Checking registration without agree")
        email = self.registration_page.getEmail()
        username = self.registration_page.getUsername()
        self.registration_page.registration(email, variables.FULL_NAME, username, variables.LOGIN_PASSWORD, False, variables.STATUS_LMS)
        #Config.doAssertTrue(self, variables.PROMPT_MESSAGE_WITHOUT_AGREE_REGISTRATION, RegistrationPage.getTextPromptMessage(self))
        self.config.do_assert_true_in(variables.PROMPT_MESSAGE_WITHOUT_AGREE_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(email, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.FULL_NAME, self.registration_page.getValueFullName())
        self.config.do_assert_true(username, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.LOGIN_PASSWORD, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_07_registration_with_smoller_full_name(self):
        '''Checking registration with smoller full name'''
        self.logger.do_test_name("Checking registration with smoller full name")
        email = self.registration_page.getEmail()
        username = self.registration_page.getUsername()
        self.registration_page.registration(email, variables.SYMBOL_A, username, variables.LOGIN_PASSWORD, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_SMALLER_FULL_NAME_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(email, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.SYMBOL_A, self.registration_page.getValueFullName())
        self.config.do_assert_true(username, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.LOGIN_PASSWORD, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_08_registration_with_smoller_username(self):
        '''Checking registration with smoller username'''
        self.logger.do_test_name("Checking registration with smoller username")
        email = self.registration_page.getEmail()
        self.registration_page.registration(email, variables.FULL_NAME, variables.SYMBOL_A, variables.LOGIN_PASSWORD, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_SMALLER_USERNAME_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(email, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.FULL_NAME, self.registration_page.getValueFullName())
        self.config.do_assert_true(variables.SYMBOL_A, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.LOGIN_PASSWORD, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_09_registration_with_smoller_password(self):
        '''Checking registration with smoller password'''
        self.logger.do_test_name("Checking registration with smoller password")
        email = self.registration_page.getEmail()
        username = self.registration_page.getUsername()
        self.registration_page.registration(email, variables.FULL_NAME, username, variables.SYMBOL_A, True, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_SMALLER_PASSWORD_REGISTRATION, self.registration_page.getTextPromptMessage())
        self.config.do_assert_true(email, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.FULL_NAME, self.registration_page.getValueFullName())
        self.config.do_assert_true(username, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.SYMBOL_A, self.registration_page.getValuePassword())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_10_password_doesnt_shown(self):
        '''Checking password doesn't shown'''
        self.logger.do_test_name("Checking password doesn't shown")
        self.login_page.input_url(variables.STATUS_LMS)
        self.registration_page.clickButtonRegistration()
        self.config.do_assert_true(variables.STATUS_PASSWORD, self.registration_page.getPasswordType())
        self.registration_page.inputPassword(variables.LOGIN_PASSWORD)
        self.config.do_assert_true(variables.STATUS_PASSWORD, self.registration_page.getPasswordType())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_11_checking_max_symbols(self):
        '''Checking max symbols'''
        self.logger.do_test_name("Checking max symbols")
        self.registration_page.registration(variables.LENGTH_FIELD_255, variables.LENGTH_FIELD_256, variables.LENGTH_FIELD_31, variables.LENGTH_FIELD_76, False, variables.STATUS_LMS)
        self.config.do_assert_true(variables.LENGTH_FIELD_254, self.registration_page.getValueEmail())
        self.config.do_assert_true(variables.LENGTH_FIELD_255, self.registration_page.getValueFullName())
        self.config.do_assert_true(variables.LENGTH_FIELD_30, self.registration_page.getValueUsername())
        self.config.do_assert_true(variables.LENGTH_FIELD_75, self.registration_page.getValuePassword())

