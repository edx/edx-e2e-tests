from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.instructor.course_info_page import CourseInfoPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.tests.main_class import MainClass
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class TestCourseInfo(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_11_reimport_courses
        '''

    def setUp(self):
        super(TestCourseInfo, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.import_page = ImportPage(self.driver)
        self.course_info_page = CourseInfoPage(self.driver)
        self.advance_settings_page = AdvancedSettingsPage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)

    def test_01_checking_course_name(self):
        '''Checking course name'''
        self.logger.do_test_name("Checking course name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_COURSE_NAME + variables.COURSE_NAME, self.course_info_page.get_info_course_information())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.advance_settings_page.open_advanced_settings()
        self.advance_settings_page.set_value_advanced_setting(variables.PATH_DISPLAY_NAME, variables.COURSE_NAME_NEW)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_false_in(variables.TEXT_COURSE_NAME + variables.COURSE_NAME, self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in(variables.TEXT_COURSE_NAME + variables.COURSE_NAME_NEW, self.course_info_page.get_info_course_information())

    def test_02_checking_course_run(self):
        '''Checking course run'''
        self.logger.do_test_name("Checking course run")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_COURSE_RUN + variables.COURSE_RUN, self.course_info_page.get_info_course_information())

    def test_03_checking_course_number(self):
        '''Checking course number'''
        self.logger.do_test_name("Checking course number")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_COURSE_NUMBER + variables.COURSE_NUMBER_POSITIVE, self.course_info_page.get_info_course_information())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.advance_settings_page.open_advanced_settings()
        self.advance_settings_page.set_value_advanced_setting(variables.PATH_COURSE_NUMBER_DISPLAY, variables.COURSE_NUMBER_NEW)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_false_in(variables.TEXT_COURSE_NUMBER + variables.COURSE_NUMBER_POSITIVE, self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in(variables.TEXT_COURSE_NUMBER + variables.COURSE_NUMBER_NEW, self.course_info_page.get_info_course_information())

    def test_04_checking_organization(self):
        '''Checking organization'''
        self.logger.do_test_name("Checking organization")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_ORGANIZATION + variables.ORGANIZATION, self.course_info_page.get_info_course_information())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.advance_settings_page.open_advanced_settings()
        self.advance_settings_page.set_value_advanced_setting(variables.PATH_ORGANIZATION_DISPLAY, variables.ORGANIZATION_NEW)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_false_in(variables.TEXT_ORGANIZATION + variables.ORGANIZATION, self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in(variables.TEXT_ORGANIZATION + variables.ORGANIZATION_NEW, self.course_info_page.get_info_course_information())

    def test_05_checking_dates(self):
        '''Checking dates'''
        self.logger.do_test_name("Checking dates")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in("Course Start Date: Jan 1, 2018", self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in("Course End Date: Jan 2, 2018", self.course_info_page.get_info_course_information())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_false_in("Course Start Date: Jan 1, 2018", self.course_info_page.get_info_course_information())
        self.config.do_assert_false_in("Course End Date: Jan 2, 2018", self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in("Course Start Date: Jan 1, 2030", self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in("Course End Date: Jan 2, 2030", self.course_info_page.get_info_course_information())

    def test_06_checking_started_yes_ended_yes(self):
        '''Checking started yes ended yes'''
        self.logger.do_test_name("Checking started yes ended yes")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_COURSE_STARTED_YES, self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in(variables.TEXT_COURSE_ENDED_YES, self.course_info_page.get_info_course_information())

    def test_07_checking_started_yes_ended_no(self):
        '''Checking started yes ended no'''
        self.logger.do_test_name("Checking started yes ended no")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_COURSE_STARTED_YES, self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in(variables.TEXT_COURSE_ENDED_NO, self.course_info_page.get_info_course_information())

    def test_08_checking_started_no_ended_no(self):
        '''Checking started no ended no'''
        self.logger.do_test_name("Checking started no ended no")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02,
                                             variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_COURSE_STARTED_NO, self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in(variables.TEXT_COURSE_ENDED_NO, self.course_info_page.get_info_course_information())

    def test_09_checking_number_of_sections(self):
        '''Checking number of sections'''
        self.logger.do_test_name("Checking number of sections")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_NUMBER_SECTIONS_2, self.course_info_page.get_info_course_information())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_ORA)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_false_in(variables.TEXT_NUMBER_SECTIONS_2, self.course_info_page.get_info_course_information())
        self.config.do_assert_true_in(variables.TEXT_NUMBER_SECTIONS_1, self.course_info_page.get_info_course_information())

    def test_10_checking_grade_cutoffs(self):
        '''Checking number of grade cutoffs'''
        self.logger.do_test_name("Checking number of grade cutoffs")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.config.do_assert_true_in(variables.TEXT_GRADE_CUTOFFS, self.course_info_page.get_info_course_information())

    def test_11_checking_step_to_git_import_logs(self):
        '''Checking step to git import logs'''
        self.logger.do_test_name("Checking step to git import logs")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_info_page.open_course_info()
        self.course_info_page.click_by_clicking_here()
        self.config.do_assert_true_in(variables.TEXT_SYSADMIN_DASHBOARD.lower(), self.sysadmin_page.get_sysadmin_text().lower())
        self.config.do_assert_true_in(variables.ORGANIZATION.lower(), self.sysadmin_page.get_sysadmin_text().lower())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE.lower(), self.sysadmin_page.get_sysadmin_text().lower())

    def test_12_reimport_courses(self):
        '''Reimport courses'''
        self.logger.do_test_name("Reimport courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
