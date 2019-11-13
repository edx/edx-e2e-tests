from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.registration_page import RegistrationPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.tests.main_class import MainClass

class TestUsers(MainClass):
    '''
        Pre-condition: Absent
        Past-condition: Absent
        '''

    def setUp(self):
        super(TestUsers, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.registration_rage = RegistrationPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.admin_page = AdminPage(self.driver)

    def test_01_create_user(self):
        '''Create user with sysadmin'''
        self.logger.do_test_name("Create user with sysadmin")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    def test_02_create_user_without_email(self):
        '''Create user without Email'''
        self.logger.do_test_name("Create user without Email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.EMPTY, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.NAME_FOR_CREATE)
        self.config.do_assert_false_in(variables.NAME_FOR_CREATE, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_EMAIL, self.login_page.get_text_prompt_message())

    def test_03_create_user_without_name(self):
        '''Create user without Full Name'''
        self.logger.do_test_name("Create user without Full Name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.EMPTY, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

    def test_04_create_user_without_password(self):
        '''Create user without Full password'''
        self.logger.do_test_name("Create user without password")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.EMPTY)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.EMPTY, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_EMPTY_PASSWORD_LOGIN, self.login_page.get_text_prompt_message())

    def test_05_create_user_with_incorrect_email(self):
        '''Create user with incorrect Email'''
        self.logger.do_test_name("Create user with incorrect Email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_BROCKEN, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_BROCKEN)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_BROCKEN, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_BROCKEN, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_EMAIL, self.login_page.get_text_prompt_message())

    def test_06_create_second_user_with_same_dataes(self):
        '''Create second user with same dataes'''
        self.logger.do_test_name("Create second user with same dataes")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        number = 2 #Count in list (One is email and other one is Name)
        self.config.do_assert_true(number, self.admin_page.get_users_list().count(variables.LOGIN_EMAIL_CREATED_USER))
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())

    def test_07_create_with_smoller_password(self):
        '''Create with smoller password'''
        self.logger.do_test_name("Create with smoller password")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.SYMBOL_A)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.SYMBOL_A, variables.STATUS_LMS)
        if (variables.PROJECT not in (variables.PROJECT_GIJIMA + variables.PROJECT_GREEN_HOST + variables.PROJECT_WARDY +
                                      variables.PROJECT_SPECTRUM + variables.PROJECT_TBS)):
            self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        else:
            self.config.do_assert_true(variables.PROMPT_MESSAGE_SMALLER_PASSWORD_REGISTRATION, self.login_page.get_text_prompt_message())

    def test_08_delete_user(self):
        '''Delete user'''
        self.logger.do_test_name("Delete user")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

    def test_09_twice_delete_user(self):
        '''Twice delete user'''
        self.logger.do_test_name("Twice delete user")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN, self.login_page.get_text_prompt_message())

    def test_10_delete_user_without_email(self):
        '''Delete user without email'''
        self.logger.do_test_name("Delete user without email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.EMPTY)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)

    def test_11_delete_user_with_incorrect_email(self):
        '''Delete user with incorrect email'''
        self.logger.do_test_name("Delete user with incorrect email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE, variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_INCORRECT)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_users()
        self.admin_page.filter_for_admin(variables.LOGIN_EMAIL_CREATED_USER)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_CREATED_USER, self.admin_page.get_users_list())
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)