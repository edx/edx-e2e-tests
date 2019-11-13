from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.lms.instructor.student_admin_page import StudentAdminPage
from e2e.main.pages.lms.progress_page import ProgressPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.registration_page import RegistrationPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.tests.main_class import MainClass

class TestUnitsActivity(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_29_reimport_courses
            '''

    def setUp(self):
        super(TestUnitsActivity, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.registration_rage = RegistrationPage(self.driver)
        self.progress_page = ProgressPage(self.driver)
        self.course_page = CoursePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.student_admin_page = StudentAdminPage(self.driver)
        self.import_page = ImportPage(self.driver)

    def test_01_course_not_graded(self):
        '''Course not graded'''
        self.logger.do_test_name("Course not graded")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_COURSE_NOT_GRATED, variables.STATUS_TRUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_false_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_COURSE_NOT_GRATED, variables.STATUS_FALSE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_02_disable_progress_graph(self):
        '''Disable progress graph'''
        self.logger.do_test_name("Delete course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_DISABLE_PROGRESS, variables.STATUS_TRUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true(variables.STATUS_OFF, self.progress_page.get_present_progress_graph())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_DISABLE_PROGRESS, variables.STATUS_FALSE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.progress_page.open_progress()
        self.config.do_assert_true(variables.STATUS_ON, self.progress_page.get_present_progress_graph())
        self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_03_maximum_attempts_free(self):
        '''Maximum attempts is free'''
        self.logger.do_test_name("Maximum attempts is free")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(1)
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())

    def test_04_maximum_attempts_on_settings(self):
        '''Maximum attempts on settings'''
        self.logger.do_test_name("Maximum attempts on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_MAXIMUM_ATTEMPTS, variables.NUMBER_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())

    def test_05_maximum_attempts_on_unit(self):
        '''Maximum attempts on unit'''
        self.logger.do_test_name("Maximum attempts on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_MAXIMUM_ATTEMPTS, variables.NUMBER_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())

    def test_06_maximum_attempts_on_settings_and_unit(self):
        '''Maximum attempts on settings and unit'''
        self.logger.do_test_name("Maximum attempts on settings and unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_MAXIMUM_ATTEMPTS, variables.NUMBER_3)
        self.course_outline_page.open_outline()
        self.course_outline_page.set_unit_settings(variables.PATH_MAXIMUM_ATTEMPTS, variables.NUMBER_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())

    def test_07_maximum_attempts_on_settings_and_unit_to_free(self):
        '''Maximum attempts on settings and unit to free'''
        self.logger.do_test_name("Maximum attempts on settings and unit to free")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_MAXIMUM_ATTEMPTS, variables.NUMBER_3)
        self.course_outline_page.open_outline()
        self.course_outline_page.set_unit_settings(variables.PATH_MAXIMUM_ATTEMPTS, variables.EMPTY)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(1)
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())

    def test_08_answer_always_on_settings(self):
        '''Answer always on settings'''
        self.logger.do_test_name("Answer always on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_ALWAYS)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_09_answer_after_answered_on_settings(self):
        '''Answer after answered on settings'''
        self.logger.do_test_name("Answer after answered on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_ANSWERED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_10_answer_after_attempted_on_settings(self):
        '''Answer after attempted on settings'''
        self.logger.do_test_name("Answer after attempted on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_ATTEMPTED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_11_answer_after_closed_on_settings(self):
        '''Answer after closed on settings'''
        self.logger.do_test_name("Answer after closed on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_CLOSED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_12_answer_after_finished_on_settings(self):
        '''Answer after finished on settings'''
        self.logger.do_test_name("Answer after finished on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_FINISHED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_13_answer_after_past_due_on_settings(self):
        '''Answer after past due on settings'''
        self.logger.do_test_name("Answer after past due on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_PAST_DUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_14_answer_correct_after_past_due_on_settings(self):
        '''Answer after answer correct or past due on settings'''
        self.logger.do_test_name("Answer after answer correct or past due on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER,
                                                               variables.ANSWER_CORRECT_PAST_DUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_15_answer_newer_doesnt_show_on_setting(self):
        '''Answer newer doesn't show on setting'''
        self.logger.do_test_name("Answer newer doesn't show on setting")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_NEWER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_16_answer_always_on_unit(self):
        '''Answer always on unit'''
        self.logger.do_test_name("Answer always on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_ALWAYS)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_17_answer_after_answered_on_unit(self):
        '''Answer after answered on unit'''
        self.logger.do_test_name("Answer after answered on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_ANSWERED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_18_answer_after_attempted_on_unit(self):
        '''Answer after attempted on unit'''
        self.logger.do_test_name("Answer after attempted on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_ATTEMPTED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_19_answer_after_closed_on_unit(self):
        '''Answer after closed on unit'''
        self.logger.do_test_name("Answer after closed on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_CLOSED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_20_answer_after_finished_on_unit(self):
        '''Answer after finished on unit'''
        self.logger.do_test_name("Answer after finished on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_FINISHED)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_21_answer_after_past_due_on_unit(self):
        '''Answer after past due on unit'''
        self.logger.do_test_name("Answer after past due on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_PAST_DUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_ON, self.course_page.get_visible_correct_result())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_22_answer_correct_after_past_due_on_unit(self):
        '''Answer after answer correct or past due on unit'''
        self.logger.do_test_name("Answer after answer correct or past due on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_CORRECT_PAST_DUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.click_show_answer()
        self.config.do_assert_true_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_23_answer_newer_doesnt_show_on_unit(self):
        '''Answer newer doesn't show on unit'''
        self.logger.do_test_name("Answer newer doesn't show on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_NEWER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_date_subsection(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_24_answer_setting_and_unit(self):
        '''Answer newer doesn't show on unit'''
        self.logger.do_test_name("Answer newer doesn't show on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_ANSWER, variables.ANSWER_ALWAYS)
        self.course_outline_page.open_outline()
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_ANSWER, variables.ANSWER_NEWER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.SHOW_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_ANSWER_ARE_DISPLAYED, self.course_page.get_about_unit_text())

    def test_25_show_calculator(self):
        '''Answer newer doesn't show on unit'''
        self.logger.do_test_name("Answer newer doesn't show on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_CALCULATOR, variables.STATUS_TRUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.click_calculator()
        self.course_page.input_calculator_value("5+7")
        self.config.do_assert_true_in("12.0", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("5-7")
        self.config.do_assert_true_in("-2.0", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("5.198+7.9864")
        self.config.do_assert_true_in("13.1844", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("5.198-7.9864")
        self.config.do_assert_true_in("-2.7884", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("100+100*100")
        self.config.do_assert_true_in("10100.0", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("(100+100)*100")
        self.config.do_assert_true_in("20000.0", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("100-7.9555/4.45")
        self.config.do_assert_true_in("98.212247191", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("-5*5")
        self.config.do_assert_true_in("-25.0", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("-5*-5")
        self.config.do_assert_true_in("25.0", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("5,198-7.9864")
        self.config.do_assert_true_in("Invalid syntax", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("5.h198-7.9864")
        self.config.do_assert_true_in("Invalid syntax", self.course_page.get_calculator_result())
        self.course_page.input_calculator_value("")
        self.config.do_assert_true_in("", self.course_page.get_calculator_result())

    def test_26_show_reset_on_settings(self):
        '''Show reset on settings'''
        self.logger.do_test_name("Show reset on settings")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_RESET, variables.STATUS_TRUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.click_reset()
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_true_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.click_reset()
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())

    def test_27_show_reset_on_unit(self):
        '''Show reset on unit'''
        self.logger.do_test_name("Show reset on unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_RESET, variables.STATUS_TRUE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.click_reset()
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_true_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.click_reset()
        self.config.do_assert_true_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        if (variables.PROJECT in (
                variables.PROJECT_DEMOUNIVERSITY + variables.PROJECT_ASUSGAB + variables.PROJECT_GREEN_HOST + variables.PROJECT_DIMINGWAY + variables.PROJECT_USDS + variables.PROJECT_SPECTRUM + variables.PROJECT_ASUOSPP)):
            self.config.do_assert_false_in(variables.PROMPT_YOU_MUST_SUBMIT, self.course_page.get_about_unit_text())

    def test_28_show_reset_on_settings_and_unit(self):
        '''Show reset on settings and unit'''
        self.logger.do_test_name("Show reset on settings and unit")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_SHOW_RESET, variables.STATUS_TRUE)
        self.course_outline_page.open_outline()
        self.course_outline_page.set_unit_settings(variables.PATH_SHOW_RESET, variables.STATUS_FALSE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_false_in(variables.RESET, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.PATH_CLASS_SHOW_ANSWER, self.course_page.get_show_answer_class())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())

    def test_29_reimport_courses(self):
        '''Reimport courses'''
        self.logger.do_test_name("Reimport courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)