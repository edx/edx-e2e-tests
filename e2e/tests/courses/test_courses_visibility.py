from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.courses_page import CoursesPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.lms.progress_page import ProgressPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.tests.main_class import MainClass
from e2e.tests.instructor.test_cohorts import variables
import unittest

class TestCoursesVisibility(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_17_enroll_second_learner
            test_18_set_ended_dates_of_course
        '''

    def setUp(self):
        super(TestCoursesVisibility, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.courses_page = CoursesPage(self.driver)
        self.course_page = CoursePage(self.driver)
        self.progress_page = ProgressPage(self.driver)
        self.import_page = ImportPage(self.driver)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_01_course_enrolling(self):
        '''Course enrolling'''
        self.logger.do_test_name("Course enrolling")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseId))
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_possible_open_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN))
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true(variables.STATUS_ON, self.courses_page.get_possible_enroll())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true_in(variables.TEXT_YOU_ARE_ENROLLED, self.courses_page.get_text_about_page())
        self.courses_page.click_view()
        self.course_page.open_course()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_02_course_invitation_only(self):
        '''Course end date'''
        self.logger.do_test_name("Course end date")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_INVITATION_ONLY, variables.STATUS_TRUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true(variables.STATUS_OFF, self.courses_page.get_possible_enroll())
        self.courses_page.click_invitation_only()
        self.courses_page.open_dashboard()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseId))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN))
        self.courses_page.open_courses()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_03_course_visibility_both(self):
        '''Course visibility both'''
        self.logger.do_test_name("Course visibility both")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true(variables.STATUS_ON, self.courses_page.get_possible_enroll())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_04_course_visibility_about(self):
        '''Course visibility about'''
        self.logger.do_test_name("Course visibility about")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_ABOUT)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_05_page_about_visibility_about(self):
        '''Course visibility about'''
        self.logger.do_test_name("Course visibility about")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_ABOUT)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        url = variables.URL_LMS + "/courses/" + courseId + "/about"
        self.config.input_url(url)
        self.config.do_assert_true(variables.STATUS_ON, self.courses_page.get_possible_enroll())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_06_course_visibility_none_new_learner(self):
        '''Course visibility none for new learner'''
        self.logger.do_test_name("Course visibility none for new learner")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    def test_07_course_visibility_none_old_learner(self):
        '''Course visibility none for old learner'''
        self.logger.do_test_name("Course visibility none for old learner")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        if(variables.PROJECT not in variables.PROJECT_ASUOSPP):
            self.courses_page.open_courses()
            self.courses_page.scroll_oll_page()
            self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_08_course_doesnt_begin(self):
        '''Course doesn't begin'''
        self.logger.do_test_name("Course doesn't begin")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true(variables.STATUS_OFF, self.courses_page.get_possible_enroll())
        self.courses_page.click_invitation_only()
        self.courses_page.open_dashboard()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseId))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN))
        self.courses_page.open_courses()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    def test_09_course_doesnt_begin_enrolled_learner(self):
        '''Course doesn't begin'''
        self.logger.do_test_name("Course doesn't begin")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseId))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN))
        if (variables.PROJECT not in variables.PROJECT_ASUOSPP):
            self.courses_page.open_courses()
            self.courses_page.scroll_oll_page()
            self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_10_course_ended(self):
        '''Course ended'''
        self.logger.do_test_name("Course ended")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    def test_11_course_ended_enrolled_learner(self):
        '''Course ended enrolled learner'''
        self.logger.do_test_name("Course ended enrolled learner")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        if (variables.PROJECT in variables.PROJECT_ASUOSPP):
            self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        else:
            self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
            self.config.do_assert_true_in(variables.VIEW_ARCHIVED_COURSE,
                                          self.dashboard_page.get_about_course_text(courseId, variables.COURSE_NUMBER_POSITIVE))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        if (variables.PROJECT not in variables.PROJECT_ASUOSPP):
            self.courses_page.open_courses()
            self.courses_page.scroll_oll_page()
            self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    def test_12_course_ended_enroll(self):
        '''Course ended enroll'''
        self.logger.do_test_name("Course ended enroll")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    def test_13_course_ended_enroll_enrolled_learner(self):
        '''Course ended enroll enrolled learner'''
        self.logger.do_test_name("Course ended enroll enrolled learner")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        if (variables.PROJECT not in variables.PROJECT_ASUOSPP):
            self.courses_page.open_courses()
            self.courses_page.scroll_oll_page()
            self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_WARDY, "Test doesn't work for Wardy IT")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_SPECTRUM, "Test doesn't work for Spectrum")
    def test_14_course_self_paced_active_dates(self):
        '''Course self paced with active dates'''
        self.logger.do_test_name("Course self paced with active dates")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.shedule_details_page.set_course_self_paced()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.course_outline_page.open_outline()
        self.course_outline_page.click_section_confrigure()
        self.config.do_assert_false_in(variables.TEXT_RELEASE_DATE, self.course_outline_page.get_text_xblock_editor_text())
        self.course_outline_page.click_cancel()
        self.course_outline_page.click_subsection_confrigure()
        self.config.do_assert_false_in(variables.TEXT_RELEASE_DATE, self.course_outline_page.get_text_xblock_editor_text())
        self.course_outline_page.click_cancel()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()


    @unittest.skipIf(variables.PROJECT == variables.PROJECT_WARDY, "Test doesn't work for Wardy IT")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_SPECTRUM, "Test doesn't work for Spectrum")
    def test_15_course_self_paced_ended_course(self):
        '''Course self paced ended course'''
        self.logger.do_test_name("Course self paced ended courses")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.shedule_details_page.set_course_self_paced()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.course_outline_page.open_outline()
        self.course_outline_page.click_section_confrigure()
        self.config.do_assert_false_in(variables.TEXT_RELEASE_DATE, self.course_outline_page.get_text_xblock_editor_text())
        self.course_outline_page.click_cancel()
        self.course_outline_page.click_subsection_confrigure()
        self.config.do_assert_false_in(variables.TEXT_RELEASE_DATE, self.course_outline_page.get_text_xblock_editor_text())
        self.course_outline_page.click_cancel()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseId))
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_possible_open_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN))
        if (variables.PROJECT not in variables.PROJECT_ASUOSPP):
            self.courses_page.open_courses()
            self.courses_page.scroll_oll_page()
            self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_WARDY, "Test doesn't work for Wardy IT")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_SPECTRUM, "Test doesn't work for Spectrum")
    def test_16_course_self_paced_doesnt_begin_course(self):
        '''Course self paced doesn't begin course'''
        self.logger.do_test_name("Course self paced doesn't begin course")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.shedule_details_page.set_course_self_paced()
        self.course_outline_page.open_outline()
        self.course_outline_page.click_section_confrigure()
        self.config.do_assert_false_in(variables.TEXT_RELEASE_DATE, self.course_outline_page.get_text_xblock_editor_text())
        self.course_outline_page.click_cancel()
        self.course_outline_page.click_subsection_confrigure()
        self.config.do_assert_false_in(variables.TEXT_RELEASE_DATE, self.course_outline_page.get_text_xblock_editor_text())
        self.course_outline_page.click_cancel()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseId))
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN))
        if (variables.PROJECT not in variables.PROJECT_ASUOSPP):
            self.courses_page.open_courses()
            self.courses_page.scroll_oll_page()
            self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    def test_17_enroll_second_learner(self):
        '''Enroll second learner'''
        self.logger.do_test_name("Enroll second learner")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_ENROLL, False, False)

    def test_18_set_ended_dates_of_course(self):
        '''Set ended dates of course'''
        self.logger.do_test_name('Set ended dates of course')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)