import unittest
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.course_team_page import CourseTeamPage
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.instructor.cohorts_page import CohortsPage
from e2e.main.pages.lms.instructor.course_info_page import CourseInfoPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.lms.discussion_page import DiscussionPage
from e2e.main.pages.lms.instructor.discussions_page import DiscussionsPage
from e2e.main.pages.gmail_page import GmailPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.instructor.student_admin_page import StudentAdminPage
from e2e.main.tests.main_class import MainClass

class TestMembership(MainClass):
    '''
        Pre-condition:
            test_01_set_variables_for_enrolling_user
            test_11_set_variables_for_enrolling_beta_tester
            test_21_set_variables
            test_39_delete_roles
        Past-condition:
            test_47_set_ended_dates_of_course
            test_48_delete_admins_roles
        '''

    def setUp(self):
        super(TestMembership, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.cohorts_page = CohortsPage(self.driver)
        self.course_info_page = CourseInfoPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.discussion_page = DiscussionPage(self.driver)
        self.discussions_page = DiscussionsPage(self.driver)
        self.gmail_page = GmailPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.student_admin_page = StudentAdminPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.course_page = CoursePage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.course_team_page = CourseTeamPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.import_page = ImportPage(self.driver)

    def test_01_set_variables_for_enrolling_user(self):
        '''Set variables for enrolling user"'''
        self.logger.do_test_name('Set variables for enrolling user')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)

    def test_02_enroll_user(self):
        '''Checking enroll user with "Auto Enroll" and with "Notify users by email"'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.dashboard_page.open_created_cours(variables.BASE_ORGANIZATION, variables.BASE_COURSE_NUMBER, variables.BASE_COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.ENROLLED, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_03_enroll_user_by_name(self):
        '''Checking enroll user by name'''
        self.logger.do_test_name('Checking enroll user by name')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.NAME_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.NAME_FIRST, "1", variables.STATUS_ENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.dashboard_page.open_created_cours(variables.BASE_ORGANIZATION, variables.BASE_COURSE_NUMBER, variables.BASE_COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.ENROLLED, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_04_unenroll_user(self):
        '''Checking unenroll user with "Auto Enroll" and with "Notify users by email"'''
        self.logger.do_test_name('Checking unenroll user with "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.UN_ENROLLED, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_05_unenroll_user_by_name(self):
        '''Checking unenroll user by name'''
        self.logger.do_test_name('Checking unenroll user by name')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.NAME_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.NAME_FIRST, "1", variables.STATUS_UNENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.UN_ENROLLED, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_06_enroll_user_without_auto_enroll(self):
        '''Checking enroll user without "Auto Enroll" and with "Notify users by email"'''
        self.logger.do_test_name('Checking enroll user without "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.dashboard_page.open_created_cours(variables.BASE_ORGANIZATION, variables.BASE_COURSE_NUMBER,
                                               variables.BASE_COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.ENROLLED, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_07_unenroll_user_without_auto_enroll(self):
        '''Checking unenroll user without "Auto Enroll" and with "Notify users by email"'''
        self.logger.do_test_name('Checking unenroll user without "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.UN_ENROLLED, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_08_enroll_user_without_notify_user(self):
        '''Checking enroll user with "Auto Enroll" and without "Notify users by email"'''
        self.logger.do_test_name('Checking enroll user with "Auto Enroll" and without "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.dashboard_page.open_created_cours(variables.BASE_ORGANIZATION, variables.BASE_COURSE_NUMBER,
                                               variables.BASE_COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        try:
            self.config.doAssertTrueIn(variables.ENROLLED, self.gmail_page.getTextFirstMessage())
        except:
            self.gmail_page.openFirstMessage()
            try:
                self.gmail_page.getTimeMessage()
            except NoSuchElementException:
                pass'''

    def test_09_unenroll_user_without_notify_user(self):
        '''Checking unenroll user with "Auto Enroll" and without "Notify users by email"'''
        self.logger.do_test_name('Checking unenroll user with "Auto Enroll" and without "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        try:
            self.config.doAssertTrueIn(variables.UN_ENROLLED, self.gmail_page.getTextFirstMessage())
        except:
            self.gmail_page.openFirstMessage()
            try:
                self.gmail_page.getTimeMessage()
            except NoSuchElementException:
                pass'''

    def test_10_enroll_not_existed_user(self):
        '''Checking enroll not existed user'''
        self.logger.do_test_name('Checking enroll not existed user')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()

        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_INCORRECT, "1", variables.STATUS_ENROLL, True, True)
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    def test_11_set_variables_for_enrolling_beta_tester(self):
        '''Set variables for enrolling user"'''
        self.logger.do_test_name('Set variables for enrolling user')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_DAYS_FOR_BETA,
                                                               variables.DAYS_FOR_BETA_TESTERS)
        self.dashboard_page.logout()

    def test_12_beta_tester_addition(self):
        '''Checking beta tester addition with "Auto Enroll" and with "Notify users by email"'''
        self.logger.do_test_name('Checking beta tester addition with "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_ENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.dashboard_page.open_created_cours(variables.BASE_ORGANIZATION, variables.BASE_COURSE_NUMBER,
                                               variables.BASE_COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.INVITED_BETA, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_13_beta_tester_addition_by_name(self):
        '''Checking beta tester addition by name'''
        self.logger.do_test_name('Checking beta tester addition by name')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.NAME_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.NAME_FIRST, variables.STATUS_ENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.dashboard_page.open_created_cours(variables.BASE_ORGANIZATION, variables.BASE_COURSE_NUMBER,
                                               variables.BASE_COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.INVITED_BETA, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_14_remove_beta_tester(self):
        '''Checking remove beta tester with "Auto Enroll" and with "Notify users by email"'''
        self.logger.do_test_name('Checking remove beta tester with "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_ENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_UNENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.REMOVED_BETA, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_15_remove_beta_tester_by_name(self):
        '''Checking remove beta tester by name'''
        self.logger.do_test_name('Checking remove beta tester by name')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.NAME_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.NAME_FIRST, variables.STATUS_ENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.NAME_FIRST, variables.STATUS_UNENROLL, True, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.REMOVED_BETA, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_16_beta_tester_addition_without_auto_enroll(self):
        '''Checking beta tester addition without "Auto Enroll" and with "Notify users by email"'''
        self.logger.do_test_name('Checking beta tester addition without "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text)

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_ENROLL, False, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.INVITED_BETA, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_17_remove_beta_tester_without_auto_enroll(self):
        '''Checking remove beta tester without "Auto Enroll" and with "Notify users by email"'''
        self.logger.do_test_name('Checking remove beta tester without "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_ENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_UNENROLL, False, True)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        self.config.doAssertTrueIn(variables.REMOVED_BETA, self.gmail_page.getTextFirstMessage())
        self.gmail_page.openFirstMessage()
        self.config.doAssertTrueIn(variables.ENROLL_TIME, self.gmail_page.getTimeMessage())
        self.gmail_page.deleteMessage()'''

    def test_18_beta_tester_addition_without_notify(self):
        '''Checking beta tester addition with "Auto Enroll" and without "Notify users by email"'''
        self.logger.do_test_name('Checking beta tester addition with "Auto Enroll" and without "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_ENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.dashboard_page.open_created_cours(variables.BASE_ORGANIZATION, variables.BASE_COURSE_NUMBER,
                                               variables.BASE_COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        try:
            self.config.doAssertTrueIn(variables.INVITED_BETA, self.gmail_page.getTextFirstMessage())
        except:
            self.gmail_page.openFirstMessage()
            try:
                self.gmail_page.getTimeMessage()
            except NoSuchElementException:
                pass'''

    def test_19_remove_beta_tester_without_notify(self):
        '''Checking remove beta tester with "Auto Enroll" and without "Notify users by email"'''
        self.logger.do_test_name('Checking remove beta tester without "Auto Enroll" and with "Notify users by email"')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_UNENROLL, False, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_false_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_ENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_FIRST, variables.STATUS_UNENROLL, True, False)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.student_admin_page.get_users_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.BASE_ORGANIZATION,
                                                                              variables.BASE_COURSE_NUMBER,
                                                                              variables.BASE_COURSE_RUN))
        self.dashboard_page.logout()

        '''self.config.inputUrl(variables.URL_EMAIL)
        self.gmail_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD_MY)
        try:
            self.config.doAssertTrueIn(variables.REMOVED_BETA, self.gmail_page.getTextFirstMessage())
        except:
            self.gmail_page.openFirstMessage()
            try:
                self.gmail_page.getTimeMessage()
            except NoSuchElementException:
                pass'''

    def test_20_enroll_not_existed_user_to_beta(self):
        '''Checking enroll not existed user to beta'''
        self.logger.do_test_name('Checking enroll not existed user to beta')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_DAYS_FOR_BETA, variables.DAYS_FOR_BETA_TESTERS)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()

        self.membership_page.open_membership()
        self.membership_page.enroll_beta_tester(variables.LOGIN_EMAIL_INCORRECT, variables.STATUS_ENROLL, True, True)
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    def test_21_set_variables(self):
        '''Set variables'''
        self.logger.do_test_name('Set variables')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

    def test_22_add_staff(self):
        '''Add staff'''
        self.logger.do_test_name('Add staff')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.config.do_assert_true_in(variables.TEXT_COURSE_OUTLINE, self.course_outline_page.get_text_course_outline_text())

    def test_23_add_staff_by_name(self):
        '''Add staff by name'''
        self.logger.do_test_name('Add staff by name')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.NAME_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.config.do_assert_true_in(variables.TEXT_COURSE_OUTLINE, self.course_outline_page.get_text_course_outline_text())

    def test_24_add_not_existed_staff(self):
        '''Add not existed staff'''
        self.logger.do_test_name('Add not existed staff')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    def test_25_add_admin(self):
        '''Add admin'''
        self.logger.do_test_name('Add admin')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_ADMIN)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_ON, self.membership_page.get_possible_add_new_role())
        self.config.do_assert_true_in(variables.ROLE_STAFF, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_ADMIN, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_BETA_TESTERS, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_DISCUSSION_ADMINS, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_DISCUSSION_MODERATORS, self.membership_page.get_role_to_add())
        if (variables.VERSION in variables.VERSION_FIKUS + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.ROLE_DISCUSSION_COMMUNITY_TAS, self.membership_page.get_role_to_add())
        else:
            self.config.do_assert_true_in(variables.ROLE_GROUP_COMMUNITY_TA, self.membership_page.get_role_to_add())
            self.config.do_assert_true_in(variables.ROLE_COMMUNITY_TA, self.membership_page.get_role_to_add())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.config.do_assert_true_in(variables.TEXT_COURSE_OUTLINE, self.course_outline_page.get_text_course_outline_text())

    def test_26_add_not_existed_admin(self):
        '''Add not existed admin'''
        self.logger.do_test_name('Add not existed admin')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.set_role(variables.ROLE_ADMIN)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    def test_27_add_beta_testers(self):
        '''Add beta testers'''
        self.logger.do_test_name('Add beta testers')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_BETA_TESTERS)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.BASE_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(variables.ID_BASE_COURSE))

    def test_28_add_not_existed_beta_testers(self):
        '''Add beta testers'''
        self.logger.do_test_name('Add beta testers')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_INCORRECT, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_BETA_TESTERS)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    def test_29_add_discussion_admins(self):
        '''Add discussion admins'''
        self.logger.do_test_name('Add discussion admins')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.set_role(variables.ROLE_DISCUSSION_ADMINS)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.delete_all_posts()
        number = self.config.get_random()
        self.discussion_page.create_post(variables.STATUS_QUESTION, variables.DISCUSSION_TITLE_STAFF + number,
                                         variables.DISCUSSION_IDEA_STAFF + number)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()

        self.config.do_assert_true(variables.STATUS_ON, self.membership_page.get_possible_add_new_role())
        self.config.do_assert_false_in(variables.ROLE_STAFF, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_ADMIN, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_BETA_TESTERS, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_DISCUSSION_ADMINS, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_DISCUSSION_MODERATORS, self.membership_page.get_role_to_add())
        if (variables.VERSION in variables.VERSION_FIKUS + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.ROLE_DISCUSSION_COMMUNITY_TAS, self.membership_page.get_role_to_add())
        else:
            self.config.do_assert_true_in(variables.ROLE_GROUP_COMMUNITY_TA, self.membership_page.get_role_to_add())
            self.config.do_assert_true_in(variables.ROLE_COMMUNITY_TA, self.membership_page.get_role_to_add())

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.open_some_discussion(variables.DISCUSSION_TITLE_STAFF + number)
        self.discussion_page.click_pin_discussion()
        self.config.do_assert_true_in(variables.TEXT_PINNED, self.discussion_page.get_labels())
        self.discussion_page.click_unpin_discussion()
        self.config.do_assert_false_in(variables.TEXT_PINNED, self.discussion_page.get_labels())

        self.discussion_page.click_report_discussion()
        self.config.do_assert_true_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())
        self.discussion_page.click_unreport_discussion()
        self.config.do_assert_false_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())

        self.discussion_page.click_close_discussion()
        self.config.do_assert_true_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_OFF, self.discussion_page.get_present_button_submit())
        self.discussion_page.click_open_discussion()
        self.config.do_assert_false_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_ON, self.discussion_page.get_present_button_submit())

        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.discussion_page.click_edit_discussion()
        self.discussion_page.input_title(variables.DISCUSSION_TITLE_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.input_idea(variables.DISCUSSION_IDEA_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.save_changes()
        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_FIRST + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_FIRST + number, self.discussion_page.get_discussion_all_text())

    def test_30_add_not_existed_discussion_admins(self):
        '''Add not existed discussion admin'''
        self.logger.do_test_name('Add not existed discussion admin')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_INCORRECT, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_DISCUSSION_ADMINS)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    def test_31_add_discussion_Moderators(self):
        '''Add discussion moderators'''
        self.logger.do_test_name('Add discussion moderators')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.set_role(variables.ROLE_DISCUSSION_MODERATORS)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.delete_all_posts()
        number = self.config.get_random()
        self.discussion_page.create_post(variables.STATUS_QUESTION, variables.DISCUSSION_TITLE_STAFF + number,
                                         variables.DISCUSSION_IDEA_STAFF + number)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.open_some_discussion(variables.DISCUSSION_TITLE_STAFF + number)
        self.discussion_page.click_pin_discussion()
        self.config.do_assert_true_in(variables.TEXT_PINNED, self.discussion_page.get_labels())
        self.discussion_page.click_unpin_discussion()
        self.config.do_assert_false_in(variables.TEXT_PINNED, self.discussion_page.get_labels())

        self.discussion_page.click_report_discussion()
        self.config.do_assert_true_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())
        self.discussion_page.click_unreport_discussion()
        self.config.do_assert_false_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())

        self.discussion_page.click_close_discussion()
        self.config.do_assert_true_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_OFF, self.discussion_page.get_present_button_submit())
        self.discussion_page.click_open_discussion()
        self.config.do_assert_false_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_ON, self.discussion_page.get_present_button_submit())

        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.discussion_page.click_edit_discussion()
        self.discussion_page.input_title(variables.DISCUSSION_TITLE_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.input_idea(variables.DISCUSSION_IDEA_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.save_changes()
        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_FIRST + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_FIRST + number, self.discussion_page.get_discussion_all_text())

    def test_32_add_not_existed_discussion_moderators(self):
        '''Add not existed discussion moderators'''
        self.logger.do_test_name('Add not existed discussion moderators')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_INCORRECT, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_DISCUSSION_MODERATORS)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_33_add_group_community(self):
        '''Add Group Community TA'''
        self.logger.do_test_name('Add Group Community TA')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        cohortName = self.cohorts_page.getCohortName()
        self.cohorts_page.addCohort(cohortName)
        self.config.do_assert_true_in(cohortName + "(0)", self.cohorts_page.get_cohorts_compound())
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(cohortName + "(1)", self.cohorts_page.get_cohorts_compound())
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_STAFF)
        self.config.do_assert_true_in(cohortName + "(2)", self.cohorts_page.get_cohorts_compound())
        self.discussions_page.open_discussions()
        self.discussions_page.set_cohorts_on()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.set_role(variables.ROLE_GROUP_COMMUNITY_TA)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.delete_all_posts()
        number = self.config.get_random()
        self.discussion_page.create_post(variables.STATUS_QUESTION, variables.DISCUSSION_TITLE_STAFF + number,
                                         variables.DISCUSSION_IDEA_STAFF + number)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.open_some_discussion(variables.DISCUSSION_TITLE_STAFF + number)
        self.discussion_page.click_pin_discussion()
        self.config.do_assert_true_in(variables.TEXT_PINNED, self.discussion_page.get_labels())
        self.discussion_page.click_unpin_discussion()
        self.config.do_assert_false_in(variables.TEXT_PINNED, self.discussion_page.get_labels())

        self.discussion_page.click_report_discussion()
        self.config.do_assert_true_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())
        self.discussion_page.click_unreport_discussion()
        self.config.do_assert_false_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())

        self.discussion_page.click_close_discussion()
        self.config.do_assert_true_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_OFF, self.discussion_page.get_present_button_submit())
        self.discussion_page.click_open_discussion()
        self.config.do_assert_false_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_ON, self.discussion_page.get_present_button_submit())

        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.discussion_page.click_edit_discussion()
        self.discussion_page.input_title(variables.DISCUSSION_TITLE_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.input_idea(variables.DISCUSSION_IDEA_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.save_changes()
        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_FIRST + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_FIRST + number, self.discussion_page.get_discussion_all_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_34_add_not_existed_group_community(self):
        '''Add not existed group community'''
        self.logger.do_test_name('Add not existed group community')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        cohortName = self.cohorts_page.getCohortName()
        self.cohorts_page.addCohort(cohortName)
        self.config.do_assert_true_in(cohortName + "(0)", self.cohorts_page.get_cohorts_compound())
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_true_in(cohortName + "(0)", self.cohorts_page.get_cohorts_compound())
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_STAFF)
        self.config.do_assert_true_in(cohortName + "(1)", self.cohorts_page.get_cohorts_compound())
        self.discussions_page.open_discussions()
        self.discussions_page.set_cohorts_on()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_INCORRECT, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_GROUP_COMMUNITY_TA)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_35_add_community(self):
        '''Add Community TA'''
        self.logger.do_test_name('Add Community TA')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.set_role(variables.ROLE_COMMUNITY_TA)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.delete_all_posts()
        number = self.config.get_random()
        self.discussion_page.create_post(variables.STATUS_QUESTION, variables.DISCUSSION_TITLE_STAFF + number,
                                         variables.DISCUSSION_IDEA_STAFF + number)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.open_some_discussion(variables.DISCUSSION_TITLE_STAFF + number)
        self.discussion_page.click_pin_discussion()
        self.config.do_assert_true_in(variables.TEXT_PINNED, self.discussion_page.get_labels())
        self.discussion_page.click_unpin_discussion()
        self.config.do_assert_false_in(variables.TEXT_PINNED, self.discussion_page.get_labels())

        self.discussion_page.click_report_discussion()
        self.config.do_assert_true_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())
        self.discussion_page.click_unreport_discussion()
        self.config.do_assert_false_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())

        self.discussion_page.click_close_discussion()
        self.config.do_assert_true_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_OFF, self.discussion_page.get_present_button_submit())
        self.discussion_page.click_open_discussion()
        self.config.do_assert_false_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_ON, self.discussion_page.get_present_button_submit())

        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.discussion_page.click_edit_discussion()
        self.discussion_page.input_title(variables.DISCUSSION_TITLE_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.input_idea(variables.DISCUSSION_IDEA_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.save_changes()
        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_FIRST + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_FIRST + number, self.discussion_page.get_discussion_all_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_36_add_not_existed_community(self):
        '''Add not existed сommunity'''
        self.logger.do_test_name('Add not existed сommunity')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_INCORRECT, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_COMMUNITY_TA)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    @unittest.skipIf(variables.VERSION == variables.VERSION_HAWTHORN, "Test doesn't work for Hawthorn")
    def test_37_add_community_tas(self):
        '''Add Community TAs'''
        self.logger.do_test_name('Add Community TAs')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_STAFF)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.set_role(variables.ROLE_DISCUSSION_COMMUNITY_TAS)
        self.config.do_assert_false_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.delete_all_posts()
        number = " " + self.config.get_random()
        self.discussion_page.create_post(variables.STATUS_QUESTION, variables.DISCUSSION_TITLE_STAFF + number,
                                         variables.DISCUSSION_IDEA_STAFF + number)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())

        self.discussion_page.open_discussion()
        self.discussion_page.open_all_discussion()
        self.discussion_page.open_some_discussion(variables.DISCUSSION_TITLE_STAFF + number)
        self.discussion_page.click_pin_discussion()
        self.config.do_assert_true_in(variables.TEXT_PINNED, self.discussion_page.get_labels())
        self.discussion_page.click_unpin_discussion()
        self.config.do_assert_false_in(variables.TEXT_PINNED, self.discussion_page.get_labels())

        self.discussion_page.click_report_discussion()
        self.config.do_assert_true_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())
        self.discussion_page.click_unreport_discussion()
        self.config.do_assert_false_in(variables.TEXT_REPORTED, self.discussion_page.get_labels())

        self.discussion_page.click_close_discussion()
        self.config.do_assert_true_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_OFF, self.discussion_page.get_present_button_submit())
        self.discussion_page.click_open_discussion()
        self.config.do_assert_false_in(variables.TEXT_CLOSED, self.discussion_page.get_labels())
        self.config.do_assert_true(variables.STATUS_ON, self.discussion_page.get_present_button_submit())

        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_IDEA_STAFF + number, self.discussion_page.get_discussion_all_text())
        self.discussion_page.click_edit_discussion()
        self.discussion_page.input_title(variables.DISCUSSION_TITLE_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.input_idea(variables.DISCUSSION_TITLE_FIRST + number, variables.STATUS_CHANGE)
        self.discussion_page.save_changes()
        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_FIRST + number, self.discussion_page.get_discussion_all_text())
        self.config.do_assert_true_in(variables.DISCUSSION_TITLE_FIRST + number, self.discussion_page.get_discussion_all_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_HAWTHORN, "Test doesn't work for Hawthorn")
    def test_38_add_not_existed_community_tas(self):
        '''Add not existed сommunity TAs'''
        self.logger.do_test_name('Add not existed сommunity TAs')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.course_info_page.open_course_info()
        text = self.course_info_page.get_info_enrollment_table_information()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_INCORRECT, "1", variables.STATUS_ENROLL, True, False)
        self.membership_page.set_role(variables.ROLE_DISCUSSION_COMMUNITY_TAS)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.membership_page.add_new_role(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.membership_page.get_team_management())
        self.course_info_page.open_course_info()
        self.config.do_assert_true(text, self.course_info_page.get_info_enrollment_table_information())

    def test_39_delete_roles(self):
        '''Add staff by course team by email'''
        self.logger.do_test_name("Add staff by course team by email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()

    def test_40_add_staff_by_course_team_by_email(self):
        '''Add staff by course team by email'''
        self.logger.do_test_name("Add staff by course team by email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())
        self.config.do_assert_false_in(variables.ROLE_STAFF, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_ADMIN, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_BETA_TESTERS, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_DISCUSSION_ADMINS, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_DISCUSSION_MODERATORS, self.membership_page.get_role_to_add())
        if (variables.VERSION in variables.VERSION_FIKUS + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.ROLE_DISCUSSION_COMMUNITY_TAS, self.membership_page.get_role_to_add())
        else:
            self.config.do_assert_false_in(variables.ROLE_GROUP_COMMUNITY_TA, self.membership_page.get_role_to_add())
            self.config.do_assert_false_in(variables.ROLE_COMMUNITY_TA, self.membership_page.get_role_to_add())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())
        self.course_outline_page.click_archived()
        self.config.do_assert_true_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())
        self.course_outline_page.open_course()
        self.config.do_assert_true_in(variables.TEXT_COURSE_OUTLINE, self.course_outline_page.get_text_course_outline_text())
        self.course_team_page.open_course_team()
        self.config.do_assert_true(variables.STATUS_OFF, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_41_add_staff_by_course_team_by_name(self):
        '''Add staff by course team by name'''
        self.logger.do_test_name("Add staff by course team by name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.NAME_FIRST)
        self.config.do_assert_true_in(variables.COULD_NOT_FIND_USER + variables.NAME_FIRST, self.course_team_page.get_prompt_message_on_page())
        self.course_team_page.click_ok()
        self.course_team_page.click_cancel()
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())
        self.course_outline_page.click_archived()
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())

    def test_42_add_staff_by_course_team_with_empty_email(self):
        '''Add staff by course team with empty email'''
        self.logger.do_test_name("Add staff by course team with empty email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.EMPTY)
        self.config.do_assert_true_in(variables.YOU_MUST_ENTER_EMAIL, self.course_team_page.get_prompt_message_on_page())
        self.course_team_page.click_ok()
        self.course_team_page.click_cancel()
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())

    def test_43_add_doesnt_registered_staff_by_course_team_to_admin(self):
        '''Add doesn't registered staff by course team to admin'''
        self.logger.do_test_name("Add doesn't registered staff by course team to admin")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_true_in(variables.COULD_NOT_FIND_USER, self.course_team_page.get_prompt_message_on_page())
        self.course_team_page.click_ok()
        self.course_team_page.click_cancel()
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_INCORRECT, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.LOGIN_EMAIL_INCORRECT, self.course_team_page.get_course_team_list())

    def test_44_delete_staff_by_course_team(self):
        '''Delete staff by course team'''
        self.logger.do_test_name("Delete staff by course team")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.course_team_page.delete_team_member(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())
        self.course_outline_page.click_archived()
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())

    def test_45_add_admin_by_course_team(self):
        '''Add admin by course team'''
        self.logger.do_test_name("Add admin by course team")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_true_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.FULL_NAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.add_admin_access(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.USERNAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_ON, self.membership_page.get_possible_add_new_role())
        self.config.do_assert_true_in(variables.ROLE_STAFF, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_ADMIN, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_BETA_TESTERS, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_DISCUSSION_ADMINS, self.membership_page.get_role_to_add())
        self.config.do_assert_true_in(variables.ROLE_DISCUSSION_MODERATORS, self.membership_page.get_role_to_add())
        if (variables.VERSION in variables.VERSION_FIKUS + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.ROLE_DISCUSSION_COMMUNITY_TAS, self.membership_page.get_role_to_add())
        else:
            self.config.do_assert_true_in(variables.ROLE_GROUP_COMMUNITY_TA, self.membership_page.get_role_to_add())
            self.config.do_assert_true_in(variables.ROLE_COMMUNITY_TA, self.membership_page.get_role_to_add())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())
        self.course_outline_page.click_archived()
        self.config.do_assert_true_in(variables.BASE_COURSE_NUMBER, self.home_page.get_courses_list_text())
        self.course_outline_page.open_course()
        self.config.do_assert_true_in(variables.TEXT_COURSE_OUTLINE, self.course_outline_page.get_text_course_outline_text())
        self.course_team_page.open_course_team()
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.USERNAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.NAME_SECOND, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.USERNAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.NAME_SECOND, self.course_team_page.get_course_team_list())

    def test_46_delete_admin_by_course_team(self):
        '''Add admin by course team'''
        self.logger.do_test_name("Add admin by course team")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.course_team_page.add_team_member(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.add_admin_access(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.USERNAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.course_team_page.remove_admin_access(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true(variables.STATUS_ON, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.USERNAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.config.do_assert_true(variables.STATUS_OFF, self.membership_page.get_possible_add_new_role())
        self.config.do_assert_false_in(variables.ROLE_STAFF, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_ADMIN, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_BETA_TESTERS, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_DISCUSSION_ADMINS, self.membership_page.get_role_to_add())
        self.config.do_assert_false_in(variables.ROLE_DISCUSSION_MODERATORS, self.membership_page.get_role_to_add())
        if (variables.VERSION in variables.VERSION_FIKUS + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.ROLE_DISCUSSION_COMMUNITY_TAS, self.membership_page.get_role_to_add())
        else:
            self.config.do_assert_false_in(variables.ROLE_GROUP_COMMUNITY_TA, self.membership_page.get_role_to_add())
            self.config.do_assert_false_in(variables.ROLE_COMMUNITY_TA, self.membership_page.get_role_to_add())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.config.do_assert_true_in(variables.TEXT_COURSE_OUTLINE, self.course_outline_page.get_text_course_outline_text())
        self.course_team_page.open_course_team()
        self.config.do_assert_true(variables.STATUS_OFF, self.course_team_page.get_present_add_team_member_button())
        self.config.do_assert_false_in(variables.ADD_NEW_TEAM_MEMBER, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_true_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.ADD_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.REMOVE_ADMIN_ACCESS, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.USERNAME_STAFF, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.DELETE_THE_USER + variables.NAME_FIRST, self.course_team_page.get_course_team_list())

    def test_47_set_ended_dates_of_course(self):
        '''Set ended dates of course'''
        self.logger.do_test_name('Set ended dates of course')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)

    def test_48_delete_admins_roles(self):
        '''Delete admins roles'''
        self.logger.do_test_name('Delete admins roles')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()

