import unittest
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

class TestUnitVisibility(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_11_reimport_courses
        '''

    def setUp(self):
        super(TestUnitVisibility, self).setUp()
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

    def test_01_unit_visible_all_positive(self):
        '''Unit visible all positive'''
        self.logger.do_test_name("Unit visible all positive")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_date_section(variables.DATE_BEFORE_TODAY_02)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_02, variables.DATE_AFTER_TODAY_01)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
            self.course_page.open_unit()
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            self.course_page.open_subsection()
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_TBS, "Test doesn't work for Toulouse BS")
    def test_02_unit_visible_off(self):
        '''Unit visible off'''
        self.logger.do_test_name("Unit visible off")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_visible(variables.STATUS_OFF)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
            self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_unit_list_text())
            self.course_page.open_unit()
            self.course_page.select_unit(1)
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            self.course_page.open_subsection()
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)

    def test_03_subsection_ended_before_today(self):
        '''Subsection ended before today'''
        self.logger.do_test_name("Subsection ended before today")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_2, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
            self.course_page.open_unit()
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            self.course_page.open_subsection()
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            pass
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)
        self.course_page.open_unit()
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())

    def test_04_subsection_started_after_today(self):
        '''Subsection started after today'''
        self.logger.do_test_name("Subsection started after today")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_date_subsection(variables.DATE_AFTER_TODAY_01, variables.DATE_AFTER_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
            self.config.do_assert_true_in(variables.SUBSECTION_NAME_2, self.course_page.get_unit_list_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            pass
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.course_page.open_section()
            self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
            self.config.do_assert_true_in(variables.SUBSECTION_NAME_2, self.course_page.get_unit_list_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)

    def test_05_subsection_set_visibility_hide_content(self):
        '''Subsection set visibility hide content'''
        self.logger.do_test_name("Subsection set visibility hide content")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.course_outline_page.set_subsection_visibility(1, 2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_2, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            pass
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_06_subsection_set_visibility_hide_entire(self):
        '''Subsection set visibility hide entire'''
        self.logger.do_test_name("Subsection set visibility hide entire")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.course_outline_page.set_subsection_visibility(1, 3)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
            self.config.do_assert_true_in(variables.SUBSECTION_NAME_2, self.course_page.get_unit_list_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
            self.config.do_assert_true_in(variables.SUBSECTION_NAME_2, self.course_page.get_unit_list_text())
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.course_page.open_section()
            self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
            self.config.do_assert_true_in(variables.SUBSECTION_NAME_2, self.course_page.get_unit_list_text())
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)
        self.progress_page.open_progress()
        self.config.do_assert_false_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_0, self.progress_page.get_grade_result_text())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_SPECTRUM, "Test doesn't work for Spectrum")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_WARDY, "Test doesn't work for Wardy IT")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_GIJIMA, "Test doesn't work for Gijima")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_TBS, "Test doesn't work for Toulouse BS")
    def test_07_subsection_set_never_show_assessment(self):
        '''Subsection set never show assessment'''
        self.logger.do_test_name("Subsection set never show assessment")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_subsection_visibility(2, 2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_SPECTRUM, "Test doesn't work for Spectrum")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_WARDY, "Test doesn't work for Wardy IT")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_GIJIMA, "Test doesn't work for Gijima")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_TBS, "Test doesn't work for Toulouse BS")
    def test_08_subsection_set_show_assessment_past_due(self):
        '''Subsection set show assessment past due'''
        self.logger.do_test_name("Subsection set show assessment past due")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.course_outline_page.set_subsection_visibility(2, 3)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())

    def test_09_section_started_after_today(self):
        '''Section started after today'''
        self.logger.do_test_name("Section started after today")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_date_section(variables.DATE_AFTER_TODAY_01)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_false_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SECTION_NAME_2, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            pass
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)

    def test_10_section_visible_off(self):
        '''Section visible off'''
        self.logger.do_test_name("Section visible off")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_section_visible()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.config.do_assert_false_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_false_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SECTION_NAME_2, self.course_page.get_unit_list_text())
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            pass
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)

    def test_11_reimport_courses(self):
        '''Reimport courses'''
        self.logger.do_test_name("Reimport courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)