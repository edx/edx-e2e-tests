import unittest
from e2e.main.pages.gmail_page import GmailPage
from e2e.main.pages.lms.account_page import AccountPage
from e2e.main.pages.lms.profile_page import ProfilePage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.tests.main_class import MainClass

class TestAccount(MainClass):
    '''
        Pre-condition: Absent
        Past-condition: Absent
        '''

    def setUp(self):
        super(TestAccount, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.account_page = AccountPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.profile_page = ProfilePage(self.driver)
        self.gmail_page = GmailPage(self.driver)

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_01_display_dataes(self):
        '''Checking display dataes on account page'''
        self.logger.do_test_name("Checking display dataes on account page")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.dashboard_page.get_name())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.account_page.get_username())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.FULL_NAME, self.account_page.get_full_name())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.account_page.get_email())
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_02_change_full_name(self):
        '''Checking changing full name'''
        self.logger.do_test_name("Checking changing full name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.NAME_FOR_CREATE, self.account_page.get_full_name())
        self.account_page.input_full_name(variables.FULL_NAME_NEW)
        self.config.do_assert_true_in(variables.FULL_NAME_NEW, self.account_page.get_full_name())
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.config.do_assert_true_in(variables.FULL_NAME_NEW, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.FULL_NAME_NEW, self.account_page.get_full_name())
        self.account_page.input_full_name(variables.NAME_FOR_CREATE)
        self.config.do_assert_true_in(variables.NAME_FOR_CREATE, self.account_page.get_full_name())
        self.profile_page.open_profile()
        self.config.do_assert_true_in(variables.NAME_FOR_CREATE, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_SPECTRUM, "Test doesn't work for SPECTRUM")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_WARDY, "Test doesn't work for Wardy IT")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_GIJIMA, "Test doesn't work for GIJIMA")
    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_03_delete_full_name_impossible(self):
        '''Checking deleting full name impossible'''
        self.logger.do_test_name("Checking deleting username impossible")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.NAME_FOR_CREATE, self.account_page.get_full_name())
        self.config.do_assert_false_in(variables.THIS_VALUE_IS_INVALID, self.account_page.get_text_all_page())
        self.account_page.input_full_name(variables.EMPTY)
        self.config.do_assert_true_in(variables.EMPTY, self.account_page.get_full_name())
        self.config.do_assert_true_in(variables.THIS_VALUE_IS_INVALID, self.account_page.get_text_all_page())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.NAME_FOR_CREATE, self.account_page.get_full_name())
        self.config.do_assert_false_in(variables.THIS_VALUE_IS_INVALID, self.account_page.get_text_all_page())
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.config.do_assert_true_in(variables.NAME_FOR_CREATE, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_04_change_email(self):
        '''Checking changing email'''
        self.logger.do_test_name("Checking changing email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.account_page.input_email(variables.GMAIL_EMAIL)
        self.config.do_assert_true_in(variables.GMAIL_EMAIL, self.account_page.get_email())
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_email()
        self.config.switch_window(0)
        self.gmail_page.delete_message()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.dashboard_page.get_name())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.GMAIL_EMAIL, self.account_page.get_email())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_05_delete_email_impossible(self):
        '''Checking delete email impossible'''
        self.logger.do_test_name("Checking delete email impossible")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.account_page.input_email(variables.EMPTY)
        self.config.do_assert_true_in(variables.EMPTY, self.account_page.get_email())
        self.config.do_assert_true_in(variables.VALID_EMAIL_ADDRESS_REQUIRED, self.account_page.get_text_all_page())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.config.do_assert_false_in(variables.VALID_EMAIL_ADDRESS_REQUIRED, self.account_page.get_text_all_page())
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_email()
        self.config.switch_window(0)

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.dashboard_page.get_name())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_06_change_email_without_confirm(self):
        '''Checking changing email without confirm'''
        self.logger.do_test_name("Checking changing email without confirm")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.account_page.input_email(variables.GMAIL_EMAIL)
        self.config.do_assert_true_in(variables.GMAIL_EMAIL, self.account_page.get_email())
        self.dashboard_page.logout()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.dashboard_page.get_name())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_07_change_email_on_existing(self):
        '''Checking changing email on existing'''
        self.logger.do_test_name("Checking changing email on existing")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.config.do_assert_false_in(variables.EMAIL_ALREADY_EXISTS, self.account_page.get_text_all_page())
        self.account_page.input_email(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_SECOND, self.account_page.get_email())
        self.config.do_assert_true_in(variables.EMAIL_ALREADY_EXISTS, self.account_page.get_text_all_page())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.config.do_assert_false_in(variables.EMAIL_ALREADY_EXISTS, self.account_page.get_text_all_page())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.dashboard_page.get_name())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_08_change_email_on_wrong(self):
        '''Checking changing email on wrong'''
        self.logger.do_test_name("Checking changing email on wrong")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.config.do_assert_false_in(variables.VALID_EMAIL_ADDRESS_REQUIRED, self.account_page.get_text_all_page())
        self.account_page.input_email(variables.LOGIN_EMAIL_BROCKEN)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_BROCKEN, self.account_page.get_email())
        self.config.do_assert_true_in(variables.VALID_EMAIL_ADDRESS_REQUIRED, self.account_page.get_text_all_page())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())
        self.config.do_assert_false_in(variables.VALID_EMAIL_ADDRESS_REQUIRED, self.account_page.get_text_all_page())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_BROCKEN, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_EMAIL, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.dashboard_page.get_name())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.account_page.get_email())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_09_change_password(self):
        '''Checking changing password'''
        self.logger.do_test_name("Checking changing password")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.add_user(variables.GMAIL_EMAIL, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.GMAIL_EMAIL, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.click_reset_password()
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_password(variables.LOGIN_PASSWORD_NEW, variables.LOGIN_PASSWORD_NEW)
        self.config.switch_window(0)
        self.gmail_page.delete_message()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_NEW, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_10_change_password_without_confirm(self):
        '''Checking changing password without confirm'''
        self.logger.do_test_name("Checking changing password without confirm")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.add_user(variables.GMAIL_EMAIL, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.GMAIL_EMAIL, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.click_reset_password()
        self.dashboard_page.logout()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_NEW, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_11_change_password_without_password(self):
        '''Checking changing password without password'''
        self.logger.do_test_name("Checking changing password without password")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.add_user(variables.GMAIL_EMAIL, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.GMAIL_EMAIL, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.click_reset_password()
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_password(variables.EMPTY, variables.EMPTY)
        self.config.switch_window(0)
        self.gmail_page.delete_message()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_NEW, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_12_change_password_without_new_password(self):
        '''Checking changing password without new password'''
        self.logger.do_test_name("Checking changing password without new password")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.add_user(variables.GMAIL_EMAIL, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.GMAIL_EMAIL, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.click_reset_password()
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_password(variables.EMPTY, variables.LOGIN_PASSWORD_NEW)
        self.config.switch_window(0)
        self.gmail_page.delete_message()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_NEW, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_13_change_password_without_confirm_password(self):
        '''Checking changing password without confirm password'''
        self.logger.do_test_name("Checking changing password without confirm password")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.add_user(variables.GMAIL_EMAIL, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.GMAIL_EMAIL, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.click_reset_password()
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_password(variables.LOGIN_PASSWORD_NEW, variables.EMPTY)
        self.config.switch_window(0)
        self.gmail_page.delete_message()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_NEW, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_14_change_password_without_same_confirm_password(self):
        '''Checking changing password without same confirm password'''
        self.logger.do_test_name("Checking changing password without same confirm password")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.add_user(variables.GMAIL_EMAIL, variables.NAME_FOR_CREATE,
                                    variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.GMAIL_EMAIL, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.click_reset_password()
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_password(variables.LOGIN_PASSWORD_NEW, variables.LOGIN_PASSWORD_INCORRECT)
        self.config.switch_window(0)
        self.gmail_page.delete_message()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_NEW, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_15_change_password_on_one_symbol(self):
        '''Checking changing password on one symbol'''
        self.logger.do_test_name("Checking changing password on one symbol")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.GMAIL_EMAIL)
        self.sysadmin_page.add_user(variables.GMAIL_EMAIL, variables.NAME_FOR_CREATE,
                                    variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.login(variables.GMAIL_EMAIL, variables.GMAIL_PASSWORD)
        self.gmail_page.open_first_message()
        self.gmail_page.delete_all()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.login_page.set_leng(variables.GMAIL_EMAIL, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.click_reset_password()
        self.dashboard_page.logout()

        self.config.input_url(variables.URL_EMAIL)
        self.gmail_page.open_first_message()
        self.gmail_page.confirm_change_password(variables.SYMBOL_A, variables.SYMBOL_A)
        self.config.switch_window(0)
        self.gmail_page.delete_message()

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_NEW, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

        self.login_page.login(variables.GMAIL_EMAIL, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_16_change_region(self):
        '''Checking changing region'''
        self.logger.do_test_name("Checking changing region")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_FIRST, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_region(variables.AUSTRIA)
        self.config.do_assert_true_in(variables.AUSTRIA_SHORT, self.account_page.get_region())
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.config.do_assert_true_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.account_page.input_region(variables.ARUBA)
        self.config.do_assert_true_in(variables.ARUBA_SHORT, self.account_page.get_region())
        self.profile_page.open_profile()
        self.config.do_assert_true_in(variables.ARUBA, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_17_change_time_zone(self):
        '''Checking changing time zone'''
        self.logger.do_test_name("Checking changing time zone")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_FIRST, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_time_zoon(variables.TIME_ZOON_AFRICA)
        self.config.do_assert_true_in(variables.TIME_ZOON_AFRICA_SHORT, self.account_page.get_time_zoon())
        self.account_page.input_time_zoon(variables.TIME_ZOON_AMERICA)
        self.config.do_assert_true_in(variables.TIME_ZOON_AMERICA_SHORT, self.account_page.get_time_zoon())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_18_change_education(self):
        '''Checking changing education'''
        self.logger.do_test_name("Checking changing education")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_FIRST, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_education(variables.DOCTORATE)
        self.config.do_assert_true_in(variables.DOCTORATE_SHORT, self.account_page.get_education())
        self.account_page.input_education(variables.ASSOCIATE_DEGREE)
        self.config.do_assert_true_in(variables.ASSOCIATE_DEGREE_SHORT, self.account_page.get_education())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_19_change_gender(self):
        '''Checking changing gender'''
        self.logger.do_test_name("Checking changing gender")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_FIRST, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_gender(variables.MALE)
        self.config.do_assert_true_in(variables.MALE_SHORT, self.account_page.get_gender())
        self.account_page.input_gender(variables.FEMALE)
        self.config.do_assert_true_in(variables.FEMALE_SHORT, self.account_page.get_gender())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_20_change_preferred_language(self):
        '''Checking changing preferred language'''
        self.logger.do_test_name("Checking changing preferred language")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_FIRST, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_preferred_language(variables.LANGUAGE_ARABIC)
        self.config.do_assert_true_in(variables.LANGUAGE_ARABIC_SHORT, self.account_page.get_preferred_language())
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.config.do_assert_true_in(variables.LANGUAGE_ARABIC, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.account_page.input_preferred_language(variables.LANGUAGE_ALBANIAN)
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN_SHORT, self.account_page.get_preferred_language())
        self.profile_page.open_profile()
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())







    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_GREEN_HOST, "Test doesn't work for Green Host")
    def test_21_delete_user(self):
        '''Checking delete user'''
        self.logger.do_test_name("Checking delete user")
        print("DELETE DOESN'T WORKING NOW")
        '''self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.LMS)
        self.sysadmin_page.openUsers()
        self.sysadmin_page.deleteUser(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.addUser(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()'''

        '''self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.LMS)
        self.account_page.open_account()
        self.logger.doClick('Delete My Account')
        self.driver.find_element_by_xpath("//button[contains(text(), 'Delete My Account')]").click()
        time.sleep(1)
        self.logger.doInput('Password = "' + LOGIN_PASSWORD_CREATED_USER + '"')
        self.driver.find_element_by_xpath("//input[@name='confirm-password']").send_keys(LOGIN_PASSWORD_CREATED_USER)
        self.logger.doClick('Yes, Delete')
        self.driver.find_element_by_xpath("//button[contains(text(), 'Delete My Account')]").click()
        time.sleep(1)'''
