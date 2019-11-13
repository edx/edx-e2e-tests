from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.certificates_cms_page import CertificatesCmsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.course_updates_page import CourseUpdatesPage
from e2e.main.pages.cms.grading_page import GradingPage
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.courses_page import CoursesPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.lms.instructor.certificates_lms_page import CertificatesLmsPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.lms.progress_page import ProgressPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.tests.main_class import MainClass
import unittest

class TestCoursesSettings(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_26_delete_created_courses
            test_27_enroll_second_learner
            test_28_reimport_courses
        '''

    def setUp(self):
        super(TestCoursesSettings, self).setUp()
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
        self.course_updates_page = CourseUpdatesPage(self.driver)
        self.grading_page = GradingPage(self.driver)
        self.certificates_lms_page = CertificatesLmsPage(self.driver)
        self.certificates_cms_page = CertificatesCmsPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.import_page = ImportPage(self.driver)

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_01_course_about_page(self):
        '''Course about page'''
        self.logger.do_test_name("Course about page")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true_in(variables.COURSE_NAME, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in("course number; " + variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_START, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_END, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_ABOUT_THIS_COURSE, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_02_course_lenguage(self):
        '''Course lenguage'''
        self.logger.do_test_name("Course lenguage")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_NEGATIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_course_lenguage(variables.TEXT_AMHARIC)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_course_lenguage(variables.TEXT_HAUSA)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE,
                                               variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.TEXT_AM, self.courses_page.get_text_refine_your_search())
        self.config.do_assert_true_in(variables.TEXT_HA, self.courses_page.get_text_refine_your_search())
        self.courses_page.search_by_refine(variables.TEXT_AM)
        self.config.do_assert_true_in(variables.TEXT_AM, self.courses_page.get_text_refine_your_search())
        self.config.do_assert_false_in(variables.TEXT_HA, self.courses_page.get_text_refine_your_search())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_false_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())
        self.courses_page.reset_search(variables.EMPTY)
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.TEXT_AM, self.courses_page.get_text_refine_your_search())
        self.config.do_assert_true_in(variables.TEXT_HA, self.courses_page.get_text_refine_your_search())
        self.courses_page.search_by_refine(variables.TEXT_HA)
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_false_in(variables.TEXT_AM, self.courses_page.get_text_refine_your_search())
        self.config.do_assert_true_in(variables.TEXT_HA, self.courses_page.get_text_refine_your_search())
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true_in(variables.COURSE_NAME, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in("course number; " + variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_START, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_END, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_ABOUT_THIS_COURSE, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_NEGATIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_DIMINGWAY, "Test doesn't work for Demingway")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_03_course_short_description(self):
        '''Course short description'''
        self.logger.do_test_name("Course short description")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_course_short_description(variables.TEXT_COURSE_SHORT_DESCRIPTION)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true_in(variables.TEXT_COURSE_SHORT_DESCRIPTION, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.COURSE_NAME, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in("course number; " + variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_START, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_END, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_ABOUT_THIS_COURSE, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_04_course_overview(self):
        '''Course overview'''
        self.logger.do_test_name("Course overview")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_course_overview(variables.FILE_PATH_COURSE_OVERVIEW)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true_in(variables.COURSE_NAME, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in("course number; " + variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_START, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_END, self.courses_page.get_text_about_page())
        self.config.do_assert_false_in(variables.TEXT_ABOUT_THIS_COURSE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_ABOUT_COURSE_INFO, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_NEW_STAFF_MEMBER_1, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_NEW_STAFF_MEMBER_2, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_05_course_correct_hours_effort(self):
        '''Course hours effort (correct value)'''
        self.logger.do_test_name("Course hours effort (correct value)")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_course_hours_effort(variables.TEXT_WEEK_WORK_HOURS)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true_in(variables.COURSE_NAME, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in("course number; " + variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_START, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_END, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_ABOUT_THIS_COURSE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_WEEK_WORK_HOURS, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_06_course_incorrect_hours_effort(self):
        '''Course hours effort (incorrect value)'''
        self.logger.do_test_name("Course hours effort (incorrect value)")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_course_hours_effort(variables.TEXT_SOME_TEXT)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_UNENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseId)
        self.config.do_assert_true_in(variables.COURSE_NAME, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in("course number; " + variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_START, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_CLASSES_END, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_ABOUT_THIS_COURSE, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(variables.TEXT_SOME_TEXT, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.TEXT_MY_COURSES, self.dashboard_page.get_my_course_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseId))
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()

    def test_07_course_license_all(self):
        '''Course license all'''
        self.logger.do_test_name("Course license all")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license_all()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_08_course_license_none(self):
        '''Course license none'''
        self.logger.do_test_name("Course license none")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license(variables.TEXT_NONCOMMERCIAL, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_NO_DERIVATIVES, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_SHARE_ALIKE, variables.STATUS_OFF)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_09_course_license_noncommercial(self):
        '''Course license noncommercial'''
        self.logger.do_test_name("Course license noncommercial")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license(variables.TEXT_NONCOMMERCIAL, variables.STATUS_ON)
        self.shedule_details_page.set_course_license(variables.TEXT_NO_DERIVATIVES, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_SHARE_ALIKE, variables.STATUS_OFF)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_10_course_license_no_derivatives(self):
        '''Course license no derivatives'''
        self.logger.do_test_name("Course license no derivatives")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license(variables.TEXT_NONCOMMERCIAL, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_NO_DERIVATIVES, variables.STATUS_ON)
        self.shedule_details_page.set_course_license(variables.TEXT_SHARE_ALIKE, variables.STATUS_OFF)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_11_course_license_share_alike(self):
        '''Course license share alike'''
        self.logger.do_test_name("Course license share alike")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license(variables.TEXT_NONCOMMERCIAL, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_NO_DERIVATIVES, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_SHARE_ALIKE, variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_12_course_license_noncommercial_and_no_derivatives(self):
        '''Course license noncommercial and no derivatives'''
        self.logger.do_test_name("Course license noncommercial and no derivatives")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license(variables.TEXT_NONCOMMERCIAL, variables.STATUS_ON)
        self.shedule_details_page.set_course_license(variables.TEXT_NO_DERIVATIVES, variables.STATUS_ON)
        self.shedule_details_page.set_course_license(variables.TEXT_SHARE_ALIKE, variables.STATUS_OFF)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_13_course_license_noncommercial_and_share_alike(self):
        '''Course license noncommercial and share alike'''
        self.logger.do_test_name("Course license noncommercial and share alike")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license(variables.TEXT_NONCOMMERCIAL, variables.STATUS_ON)
        self.shedule_details_page.set_course_license(variables.TEXT_NO_DERIVATIVES, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_SHARE_ALIKE, variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_14_course_license_no_deriavatives_and_share_alike(self):
        '''Course license no deriavatives and share alike'''
        self.logger.do_test_name("Course license no deriavatives and share alike")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.set_course_license(variables.TEXT_NONCOMMERCIAL, variables.STATUS_OFF)
        self.shedule_details_page.set_course_license(variables.TEXT_NO_DERIVATIVES, variables.STATUS_ON)
        self.shedule_details_page.set_course_license(variables.TEXT_SHARE_ALIKE, variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_ALL_RIGHTS_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_RIGHT_RESERVED, self.course_page.get_licenses_text())
        self.config.do_assert_false_in("©", self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_ATTRIBUTION, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NONCOMMERCIAL, self.course_page.get_licenses_text())
        self.config.do_assert_false_in(variables.TEXT_NO_DERIVATIVES, self.course_page.get_licenses_text())
        self.config.do_assert_true_in(variables.TEXT_SHARE_ALIKE, self.course_page.get_licenses_text())

    def test_15_input_course_updates(self):
        '''Input course updates and course handouts'''
        self.logger.do_test_name("Input course updates and course handouts")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.course_updates_page.open_course_updates()
        self.course_updates_page.input_course_update(variables.TEXT_COURSE_UPDATES)
        self.course_updates_page.input_course_handouts(variables.TEXT_COURSE_HANDOUTS)
        self.config.do_assert_true_in(variables.TEXT_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.config.do_assert_true_in(variables.TEXT_COURSE_HANDOUTS, self.course_updates_page.get_about_course_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        if (variables.PROJECT not in variables.PROJECT_GREEN_HOST):
            self.config.do_assert_true_in(variables.TEXT_COURSE_UPDATES, self.course_page.get_course_content_text())
        self.config.do_assert_true_in(variables.TEXT_COURSE_HANDOUTS, self.course_page.get_course_content_text())
        if (variables.PROJECT not in variables.PROJECT_GREEN_HOST + variables.PROJECT_ASUOSPP + variables.PROJECT_TBS + variables.PROJECT_SPECTRUM):
            self.course_page.open_updates()
            self.config.do_assert_true_in(variables.TEXT_COURSE_UPDATES, self.course_page.get_course_content_text())

    def test_16_change_course_updates(self):
        '''Change course updates and course handouts'''
        self.logger.do_test_name("Input course updates and course handouts")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_updates_page.open_course_updates()
        self.course_updates_page.input_course_update(variables.TEXT_COURSE_UPDATES)
        self.course_updates_page.input_course_handouts(variables.TEXT_COURSE_HANDOUTS)
        self.config.do_assert_true_in(variables.TEXT_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.config.do_assert_true_in(variables.TEXT_COURSE_HANDOUTS, self.course_updates_page.get_about_course_text())
        self.course_updates_page.edit_course_update(variables.TEXT_NEW_COURSE_UPDATES)
        self.course_updates_page.input_course_handouts(variables.TEXT_NEW_COURSE_HANDOUTS)
        self.config.do_assert_false_in(variables.TEXT_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.config.do_assert_false_in(variables.TEXT_COURSE_HANDOUTS, self.course_updates_page.get_about_course_text())
        self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_HANDOUTS, self.course_updates_page.get_about_course_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        if (variables.PROJECT not in variables.PROJECT_GREEN_HOST):
            self.config.do_assert_false_in(variables.TEXT_COURSE_UPDATES, self.course_page.get_course_content_text())
            self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_UPDATES, self.course_page.get_course_content_text())
        self.config.do_assert_false_in(variables.TEXT_COURSE_HANDOUTS, self.course_page.get_course_content_text())
        self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_HANDOUTS, self.course_page.get_course_content_text())
        if (variables.PROJECT not in variables.PROJECT_GREEN_HOST + variables.PROJECT_ASUOSPP + variables.PROJECT_TBS + variables.PROJECT_SPECTRUM):
            self.course_page.open_updates()
            self.config.do_assert_false_in(variables.TEXT_COURSE_UPDATES, self.course_page.get_course_content_text())
            self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_UPDATES, self.course_page.get_course_content_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_GREEN_HOST, "Test doesn't work for Green Host")
    def test_17_input_few_course_updates(self):
        '''Input few course updates'''
        self.logger.do_test_name("Input few course updates")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_updates_page.open_course_updates()
        self.course_updates_page.input_course_update(variables.TEXT_COURSE_UPDATES)
        self.course_updates_page.input_course_update(variables.TEXT_NEW_COURSE_UPDATES)
        self.config.do_assert_true_in(variables.TEXT_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.config.do_assert_false_in(variables.TEXT_COURSE_UPDATES, self.course_page.get_course_content_text())
        self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_UPDATES, self.course_page.get_course_content_text())
        if (variables.PROJECT not in variables.PROJECT_GREEN_HOST):
            self.course_page.open_updates()
            self.config.do_assert_true_in(variables.TEXT_COURSE_UPDATES, self.course_page.get_course_content_text())
            self.config.do_assert_true_in(variables.TEXT_NEW_COURSE_UPDATES, self.course_page.get_course_content_text())

    def test_18_delete_course_updates(self):
        '''Delete course updates and course handouts'''
        self.logger.do_test_name("Input course updates and course handouts")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_updates_page.open_course_updates()
        self.course_updates_page.input_course_update(variables.TEXT_COURSE_UPDATES)
        self.course_updates_page.input_course_handouts(variables.TEXT_COURSE_HANDOUTS)
        self.config.do_assert_true_in(variables.TEXT_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.config.do_assert_true_in(variables.TEXT_COURSE_HANDOUTS, self.course_updates_page.get_about_course_text())
        self.course_updates_page.delete_course_update()
        self.course_updates_page.input_course_handouts(variables.EMPTY)
        self.config.do_assert_false_in(variables.TEXT_COURSE_UPDATES, self.course_updates_page.get_about_course_text())
        self.config.do_assert_false_in(variables.TEXT_COURSE_HANDOUTS, self.course_updates_page.get_about_course_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.config.do_assert_false_in(variables.TEXT_COURSE_UPDATES, self.course_page.get_course_content_text())
        self.config.do_assert_false_in(variables.TEXT_COURSE_HANDOUTS, self.course_page.get_course_content_text())

    def test_19_input_course_display_name(self):
        '''Input course display name'''
        self.logger.do_test_name("Input course display name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_DISPLAY_NAME, variables.NEW_COURSE_NAME)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.config.do_assert_true_in(variables.NEW_COURSE_NAME, self.dashboard_page.get_dashboard_courses_list_text())
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()

    def test_20_link_to_prerequisite_course(self):
        '''Link to prerequisite course'''
        self.logger.do_test_name("Link to prerequisite course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseNameFirst = variables.COURSE_NAME + " " + self.config.get_random()
        courseNameSecond = variables.COURSE_NAME_SECOND + " " + self.config.get_random()
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumberFirst = self.config.get_random()
        courseNumberSecond = self.config.get_random()
        courseRun = variables.COURSE_RUN
        courseIdFirst = variables.ID + organization + "+" + courseNumberFirst + "+" + courseRun
        courseIdSecond = variables.ID + organization + "+" + courseNumberSecond + "+" + courseRun
        namePrerequisiteCourse = organization + " " + courseNumberFirst
        self.course_outline_page.create_course(courseNameFirst, organization, courseNumberFirst, courseRun)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.home_page.open_home()
        self.course_outline_page.create_course(courseNameSecond, organization, courseNumberSecond, courseRun)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.shedule_details_page.set_prerequisite_course(courseNameFirst)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseIdSecond)
        self.config.do_assert_true_in(namePrerequisiteCourse, self.courses_page.get_text_about_page())
        self.config.do_assert_false_in(courseNameFirst, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(courseNameSecond, self.courses_page.get_text_about_page())
        self.courses_page.open_prerequisites_course(namePrerequisiteCourse)
        self.config.do_assert_true_in(courseNameFirst, self.courses_page.get_text_about_page())
        self.config.do_assert_false_in(courseNameSecond, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true_in(courseNameFirst, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseIdFirst))
        self.config.do_assert_false_in(courseNameSecond, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseIdSecond))
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseIdSecond)
        self.config.do_assert_false_in(courseNameFirst, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(courseNameSecond, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.dashboard_page.get_possible_open_course(organization, courseNumberSecond, courseRun))
        self.config.do_assert_true_in(courseNameFirst, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseIdFirst))
        self.config.do_assert_true_in(courseNameSecond, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseIdSecond))
        self.config.do_assert_true_in(namePrerequisiteCourse, self.dashboard_page.get_dashboard_courses_list_text())
        self.dashboard_page.open_prerequisites_course(namePrerequisiteCourse)
        self.config.do_assert_true_in(courseNameFirst, self.courses_page.get_text_about_page())
        self.config.do_assert_false_in(courseNameSecond, self.courses_page.get_text_about_page())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.sysadmin_page.delete_created_courses()

    def test_21_delete_prerequisite_course(self):
        '''Delete prerequisite course'''
        self.logger.do_test_name("Delete prerequisite course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseNameFirst = variables.COURSE_NAME + " " + self.config.get_random()
        courseNameSecond = variables.COURSE_NAME_SECOND + " " + self.config.get_random()
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumberFirst = self.config.get_random()
        courseNumberSecond = self.config.get_random()
        courseRun = variables.COURSE_RUN
        courseIdFirst = variables.ID + organization + "+" + courseNumberFirst + "+" + courseRun
        courseIdSecond = variables.ID + organization + "+" + courseNumberSecond + "+" + courseRun
        namePrerequisiteCourse = organization + " " + courseNumberFirst
        self.course_outline_page.create_course(courseNameFirst, organization, courseNumberFirst, courseRun)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.home_page.open_home()
        self.course_outline_page.create_course(courseNameSecond, organization, courseNumberSecond, courseRun)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.shedule_details_page.set_prerequisite_course(courseNameFirst)
        self.shedule_details_page.set_prerequisite_course(variables.STATUS_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseIdSecond)
        self.config.do_assert_false_in(namePrerequisiteCourse, self.courses_page.get_text_about_page())
        self.config.do_assert_false_in(courseNameFirst, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(courseNameSecond, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_false_in(courseNameFirst, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseIdFirst))
        self.config.do_assert_true_in(courseNameSecond, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseIdSecond))
        self.config.do_assert_false_in(namePrerequisiteCourse, self.dashboard_page.get_dashboard_courses_list_text())
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.courses_page.open_created_course(courseIdFirst)
        self.config.do_assert_false_in(namePrerequisiteCourse, self.courses_page.get_text_about_page())
        self.config.do_assert_true_in(courseNameFirst, self.courses_page.get_text_about_page())
        self.config.do_assert_false_in(courseNameSecond, self.courses_page.get_text_about_page())
        self.courses_page.click_enroll()
        self.config.do_assert_true_in(courseNameFirst, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseIdFirst))
        self.config.do_assert_true_in(courseNameSecond, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseIdSecond))
        self.config.do_assert_false_in(namePrerequisiteCourse, self.dashboard_page.get_dashboard_courses_list_text())
        self.dashboard_page.open_created_cours(organization, courseNumberFirst, courseRun)
        self.course_page.open_course()
        self.courses_page.open_dashboard()
        self.dashboard_page.open_created_cours(organization, courseNumberSecond, courseRun)
        self.course_page.open_course()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.sysadmin_page.delete_created_courses()

    def test_22_complete_prerequisite_course(self):
        '''Complete prerequisite course'''
        self.logger.do_test_name("Complete prerequisite course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseNameFirst = variables.COURSE_NAME + " " + self.config.get_random()
        courseNameSecond = variables.COURSE_NAME_SECOND + " " + self.config.get_random()
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumberFirst = self.config.get_random()
        courseNumberSecond = self.config.get_random()
        courseRun = variables.COURSE_RUN
        self.course_outline_page.create_course(courseNameFirst, organization, courseNumberFirst, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.grading_page.open_grading()
        self.grading_page.delete_all_types()
        self.grading_page.create_type(variables.TEXT_HOMEWORK, variables.TEXT_HW, variables.NUMBER_100, variables.NUMBER_1,
                                      variables.NUMBER_0)
        self.course_outline_page.open_outline()
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.home_page.open_home()
        self.course_outline_page.create_course(courseNameSecond, organization, courseNumberSecond, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.shedule_details_page.set_prerequisite_course(courseNameFirst)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.set_certificate_generation(variables.STATUS_ON)
        self.admin_page.set_certificate_html(variables.STATUS_ON)
        courseId = variables.ID + organization + "+" + courseNumberFirst + "+" + courseRun
        self.admin_page.set_course_modes(courseId, variables.STATUS_MODE_HONOR, variables.TEXT_TEST)
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(organization, courseNumberFirst, courseRun)
        self.certificates_cms_page.open_certificates()
        self.certificates_cms_page.setup_certificate()
        self.certificates_cms_page.activate_certificate()
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CERTIFICATES_DISPLAY_BEHAVIOR,
                                                               variables.EARLY_NO_INFO)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumberSecond, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.courses_page.open_dashboard()
        self.dashboard_page.open_created_cours(organization, courseNumberFirst, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.certificates_lms_page.open_certificates()
        self.certificates_lms_page.set_certificates(variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumberFirst, courseRun)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.course_page.correct_answer_unit(2)
        self.course_page.correct_answer_unit(3)
        self.progress_page.open_progress()
        self.progress_page.click_request_certificate()
        self.courses_page.open_dashboard()
        self.dashboard_page.open_created_cours(organization, courseNumberSecond, courseRun)
        self.course_page.open_course()

    def test_23_obligatory_complete_prerequisite_course(self):
        '''Obligatory сomplete prerequisite course'''
        self.logger.do_test_name("Obligatory сomplete prerequisite course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseNameFirst = variables.COURSE_NAME + " " + self.config.get_random()
        courseNameSecond = variables.COURSE_NAME_SECOND + " " + self.config.get_random()
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumberFirst = self.config.get_random()
        courseNumberSecond = self.config.get_random()
        courseRun = variables.COURSE_RUN
        courseIdFirst = variables.ID + organization + "+" + courseNumberFirst + "+" + courseRun
        courseIdSecond = variables.ID + organization + "+" + courseNumberSecond + "+" + courseRun
        self.course_outline_page.create_course(courseNameFirst, organization, courseNumberFirst, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.grading_page.open_grading()
        self.grading_page.delete_all_types()
        self.grading_page.create_type(variables.TEXT_HOMEWORK, variables.TEXT_HW, variables.NUMBER_100, variables.NUMBER_1,
                                      variables.NUMBER_0)
        self.course_outline_page.open_outline()
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.home_page.open_home()
        self.course_outline_page.create_course(courseNameSecond, organization, courseNumberSecond, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.shedule_details_page.set_prerequisite_course(courseNameFirst)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.set_certificate_generation(variables.STATUS_ON)
        self.admin_page.set_certificate_html(variables.STATUS_ON)
        courseId = variables.ID + organization + "+" + courseNumberFirst + "+" + courseRun
        self.admin_page.set_course_modes(courseId, variables.STATUS_MODE_HONOR, variables.TEXT_TEST)
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(organization, courseNumberFirst, courseRun)
        self.certificates_cms_page.open_certificates()
        self.certificates_cms_page.setup_certificate()
        self.certificates_cms_page.activate_certificate()
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CERTIFICATES_DISPLAY_BEHAVIOR,
                                                               variables.EARLY_NO_INFO)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumberSecond, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.courses_page.open_dashboard()
        self.dashboard_page.open_created_cours(organization, courseNumberFirst, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, True, False)
        self.certificates_lms_page.open_certificates()
        self.certificates_lms_page.set_certificates(variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumberFirst, courseRun)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.course_page.incorrect_answer_unit(2)
        self.course_page.incorrect_answer_unit(3)
        self.progress_page.open_progress()
        self.config.do_assert_true(variables.STATUS_OFF, self.progress_page.get_present_request_certificate())
        self.courses_page.open_dashboard()
        self.config.do_assert_true_in(courseNameFirst, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_ON, self.dashboard_page.get_present_button_view_course(courseIdFirst))
        self.config.do_assert_true_in(courseNameSecond, self.dashboard_page.get_dashboard_courses_list_text())
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_present_button_view_course(courseIdSecond))
        self.config.do_assert_true(variables.STATUS_OFF, self.dashboard_page.get_possible_open_course(organization, courseNumberSecond, courseRun))

    def test_24_complete_entrance_exam(self):
        '''Complete entrance exam'''
        self.logger.do_test_name("Complete entrance exam")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_course_number()
        courseRun = variables.COURSE_RUN
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.shedule_details_page.set_entrance_exam()
        self.course_outline_page.open_outline()
        self.course_outline_page.add_unit(variables.UNIT_NAME_EXAM, variables.EMPTY, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_EXAM, variables.EMPTY, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_EXAM, variables.EMPTY, variables.BLOCK_MULTIPLE_CHOICE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumber, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.config.do_assert_false_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.course_page.correct_answer_unit(1)
        self.course_page.correct_answer_unit(2)
        self.course_page.incorrect_answer_unit(3)
        self.config.refresh_page()
        self.course_page.click_next()
        self.course_page.click_next()
        self.course_page.click_next()
        self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())

    def test_25_obligatory_complete_entrance_exam(self):
        '''Obligatory complete entrance exam'''
        self.logger.do_test_name("Obligatory complete entrance exam")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_course_number()
        courseRun = variables.COURSE_RUN
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.TEXT_HOMEWORK, variables.BLOCK_MULTIPLE_CHOICE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.shedule_details_page.set_entrance_exam()
        self.course_outline_page.open_outline()
        self.course_outline_page.add_unit(variables.UNIT_NAME_EXAM, variables.EMPTY, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_EXAM, variables.EMPTY, variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_EXAM, variables.EMPTY, variables.BLOCK_MULTIPLE_CHOICE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumber, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.config.do_assert_false_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.course_page.correct_answer_unit(1)
        self.course_page.incorrect_answer_unit(2)
        self.course_page.incorrect_answer_unit(3)
        self.config.refresh_page()
        self.course_page.click_next()
        self.course_page.click_next()
        self.course_page.click_next()
        self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.course_page.open_course()
        self.config.do_assert_false_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())

    def test_26_delete_created_courses(self):
        '''Deleting all created courses'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.sysadmin_page.delete_created_courses()

    def test_27_enroll_second_learner(self):
        '''Enroll second learner'''
        self.logger.do_test_name("Enroll second learner")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_ENROLL, False, False)

    def test_28_reimport_courses(self):
        '''Reimport courses'''
        self.logger.do_test_name("Reimport courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)