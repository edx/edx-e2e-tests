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

class TestCoursesSearch(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_07_reimport_courses
                test_08_set_ended_dates_of_course
        '''

    def setUp(self):
        super(TestCoursesSearch, self).setUp()
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
    def test_01_course_search_by_number_on_courses_page(self):
        '''Course search by number on courses page'''
        self.logger.do_test_name("Course search by number on courses page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.search_by_text(variables.COURSE_NUMBER_POSITIVE)
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_false_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())
        self.courses_page.search_by_text(variables.COURSE_NUMBER_NEGATIVE)
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_02_course_search_by_name_on_courses_page(self):
        '''Course search by name on courses page'''
        self.logger.do_test_name("Course search by name on courses page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY,
                                                               variables.STATUS_VISIBILITY_BOTH)

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.search_by_text(variables.COURSE_NUMBER_POSITIVE)
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.courses_page.get_courses_list_text())
        self.courses_page.search_by_text(variables.BASE_COURSE_NAME)
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.BASE_COURSE_NUMBER, self.courses_page.get_courses_list_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_03_course_search_by_about_text_on_courses_page(self):
        '''Course search by about text on courses page'''
        self.logger.do_test_name("Course search by about text on courses page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_course_overview(variables.FILE_PATH_COURSE_OVERVIEW_FOR_SEARCH)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.search_by_text(variables.SOME_INDIVIDUAL_TEXT)
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_false_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())
        self.courses_page.search_by_text(variables.TEXT_ABOUT_THIS_COURSE)
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_04_course_search_by_empty_field_on_courses_page(self):
        '''Course search by empty field on courses page'''
        self.logger.do_test_name("Course search by empty field on courses page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.search_by_text(variables.EMPTY)
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_NEGATIVE, self.courses_page.get_courses_list_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_05_course_search_by_table_on_courses_page(self):
        '''Course search by table on courses page'''
        self.logger.do_test_name("Course search by table on courses page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_BOTH)
        self.home_page.open_home()
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.courses_page.open_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.BASE_COURSE_NUMBER, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.courses_page.search_by_refine(variables.BASE_ORGANIZATION)
        self.config.do_assert_true_in(variables.BASE_COURSE_NUMBER, self.courses_page.get_courses_list_text())
        self.config.do_assert_false_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.courses_page.reset_search(variables.BASE_ORGANIZATION)
        self.courses_page.search_by_refine(variables.ORGANIZATION)
        self.config.do_assert_false_in(variables.BASE_COURSE_NUMBER, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.courses_page.reset_search(variables.EMPTY)
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.BASE_COURSE_NUMBER, self.courses_page.get_courses_list_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASUOSPP")
    def test_06_course_search_by_text_on_unit_page(self):
        '''Course search by text on unit page'''
        self.logger.do_test_name("Course search by text on unit page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.search_course(variables.BLOCK_MULTIPLE_CHOICE)
        self.config.do_assert_true_in(variables.SEARCH_RESULTS, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.UNIT_NAME_3, self.course_page.get_about_unit_text())
        self.course_page.click_view()
        self.config.do_assert_true_in(variables.BLOCK_MULTIPLE_CHOICE, self.course_page.get_about_unit_text())
        self.course_page.open_course()
        self.course_page.search_course(variables.BLOCK_CHECKBOXES)
        self.config.do_assert_true_in(variables.SEARCH_RESULTS, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_3, self.course_page.get_about_unit_text())
        self.course_page.click_view()
        self.config.do_assert_true_in(variables.BLOCK_CHECKBOXES, self.course_page.get_about_unit_text())
        self.course_page.open_course()
        self.course_page.search_course(variables.TEXT_SOME_TEXT)
        self.config.do_assert_true_in(variables.SEARCH_RESULTS, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_3, self.course_page.get_about_unit_text())
        self.course_page.open_course()
        if(variables.VERSION in variables.VERSION_FIKUS):
            textOnPage = self.course_page.get_about_unit_text()
            self.course_page.search_course(variables.EMPTY)
            self.config.do_assert_true_in(textOnPage, self.course_page.get_about_unit_text())
        else:
            self.course_page.search_course(variables.EMPTY)
            self.config.do_assert_true_in(variables.SEARCH_RESULTS, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.NO_RESULTS_FOUND, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_3, self.course_page.get_about_unit_text())
        self.course_page.search_course(variables.NUMBER_1)
        self.config.do_assert_true_in(variables.SEARCH_RESULTS, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.NO_RESULTS_FOUND, self.course_page.get_about_unit_text())
        if(variables.VERSION in variables.VERSION_FIKUS):
            pass
        else:
            self.config.do_assert_false_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_3, self.course_page.get_about_unit_text())

    def test_07_reimport_courses(self):
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

    def test_08_set_ended_dates_of_course(self):
        '''Set ended dates of course'''
        self.logger.do_test_name('Set ended dates of course')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)