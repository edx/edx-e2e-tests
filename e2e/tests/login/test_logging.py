from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.tests.main_class import MainClass

class TestLogging(MainClass):
    '''
        Pre-condition: Absent
        Past-condition: Absent
        '''

    def setUp(self):
        super(TestLogging, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def test_01_logging_with_correct_dataes(self):
        '''Checking logging user'''
        self.logger.do_test_name("Checking logging user")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    def test_02_logging_with_incorrect_email(self):
        '''Checking logging user with incorrect email'''
        self.logger.do_test_name("Checking logging user with incorrec t email")
        self.login_page.login(variables.LOGIN_EMAIL_INCORRECT, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

    def test_03_logging_with_incorrect_password(self):
        '''Checking logging user with incorrect password'''
        self.logger.do_test_name("Checking logging user with incorrect password")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_INCORRECT, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

    def test_04_logging_without_email(self):
        '''Checking logging user without email'''
        self.logger.do_test_name("Checking logging user without email")
        self.login_page.login(variables.EMPTY, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_EMPTY_EMAIL_LOGIN, self.login_page.get_text_prompt_message())

    def test_05_logging_without_password(self):
        '''Checking logging user without password'''
        self.logger.do_test_name("Checking logging user without password")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.EMPTY, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_EMPTY_PASSWORD_LOGIN, self.login_page.get_text_prompt_message())

    def test_06_password_doesnt_shown(self):
        '''Checking password doesn't shown'''
        self.logger.do_test_name("Checking password doesn't shown")
        self.login_page.input_url(variables.STATUS_LMS)
        self.login_page.click_sign_in_button(variables.STATUS_LMS)
        self.config.do_assert_true(variables.STATUS_PASSWORD, self.login_page.get_password_type())
        self.login_page.input_password(variables.LOGIN_PASSWORD)
        self.config.do_assert_true(variables.STATUS_PASSWORD, self.login_page.get_password_type())