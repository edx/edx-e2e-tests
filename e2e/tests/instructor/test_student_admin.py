import unittest
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.instructor.student_admin_page import StudentAdminPage
from e2e.main.pages.lms.progress_page import ProgressPage
from e2e.main.pages.login_page import *
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.tests.main_class import MainClass
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class TestStudentAdmin(MainClass):
    '''
        Pre-condition:
            test_00_set_values
        Past-condition:
            test_28_reimport_courses
        '''

    def setUp(self):
        super(TestStudentAdmin, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_page = CoursePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.student_admin_page = StudentAdminPage(self.driver)
        self.import_page = ImportPage(self.driver)
        self.progress_page = ProgressPage(self.driver)
        self.home_page = HomePage(self.driver)

    def test_00_set_values(self):
        '''Set values'''
        self.logger.do_test_name("Set values")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_MAXIMUM_ATTEMPTS, variables.NUMBER_1)

    def test_01_view_gradebook(self):
        '''View gradebook'''
        self.logger.do_test_name("View gradebook")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.course_page.correct_answer_unit(2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_gradebook()
        self.config.do_assert_true_in(variables.NAME_FIRST + '; ' + variables.NAME_SECOND, self.student_admin_page.get_users_list_text())
        self.config.do_assert_true_in("33 33; 67 67", self.student_admin_page.get_users_list_text())

    def test_02_view_learners_progress_by_email(self):
        '''View learners progress by email'''
        self.logger.do_test_name("View learners progress by email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.course_page.correct_answer_unit(2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_learners_progress(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_learners_progress(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_true_in(variables.TEXT_GRADE_67, self.progress_page.get_grade_result_text())

    def test_03_view_learners_progress_by_name(self):
        '''View learners progress by name'''
        self.logger.do_test_name("View learners progress by name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_learners_progress(variables.NAME_FIRST)
        self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_04_view_learners_progress_by_empty_email(self):
        '''View learners progress by empty email'''
        self.logger.do_test_name("View learners progress by empty email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_learners_progress(variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_STUDENT_EMAIL, self.student_admin_page.get_page_text())

    def test_05_view_learners_progress_by_incorrect_email(self):
        '''View learners progress by incorrect email'''
        self.logger.do_test_name("View learners progress by incorrect email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.open_learners_progress(variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_STUDENT_INDENTINIER, self.student_admin_page.get_page_text())

    def test_06_reset_learners_attempts(self):
        '''Reset learners attempts'''
        self.logger.do_test_name("Reset learners attempts")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.reset_attempts(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_07_reset_learners_attempts_without_correct_email(self):
        '''Reset learners attempts without correct email'''
        self.logger.do_test_name("Reset learners attempts without correct email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.reset_attempts(variables.EMPTY, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_STUDENT_EMAIL, self.student_admin_page.get_page_text())

        self.student_admin_page.reset_attempts(variables.LOGIN_EMAIL_INCORRECT, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER, self.student_admin_page.get_page_text())

    def test_08_reset_learners_attempts_without_correct_unit_id(self):
        '''Reset learners attempts without correct unit id'''
        self.logger.do_test_name("Reset learners attempts without correct unit id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.reset_attempts(variables.LOGIN_EMAIL_FIRST, variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.reset_attempts(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1 + "1")
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER, self.student_admin_page.get_page_text())

        self.student_admin_page.reset_attempts(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.reset_attempts(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.course_page.open_course()

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_09_override_learners_score(self):
        '''Override learners score'''
        self.logger.do_test_name("Override learners score")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.override_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1, "0.5")
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_HULF_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_17, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_10_override_learners_score_on_not_valid(self):
        '''Override learners score on not valid'''
        self.logger.do_test_name("Override learners score on not valid")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.override_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1, variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_SCORE, self.student_admin_page.get_page_text())

        self.student_admin_page.override_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1, "1.5")
        self.config.do_assert_true_in(variables.PROMPT_SCORE_MUST_BE, self.student_admin_page.get_page_text())

        self.student_admin_page.override_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1, "1,5")
        self.config.do_assert_true_in(variables.PROMPT_INVALID_LITERAL_FOR_FLOAT, self.student_admin_page.get_page_text())

        self.student_admin_page.override_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1, variables.TEXT_SOME_TEXT)
        self.config.do_assert_true_in(variables.PROMPT_COULD_NOT_CONVERT_SCORE, self.student_admin_page.get_page_text())

    def test_11_delete_learners_state(self):
        '''Delete learners state'''
        self.logger.do_test_name("Delete learners state")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_0_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_0, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_12_delete_learners_state_without_correct_email(self):
        '''Delete learners state without correct email'''
        self.logger.do_test_name("Delete learners state without correct email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_learners_state(variables.EMPTY, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_STUDENT_EMAIL, self.student_admin_page.get_page_text())

        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_INCORRECT, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER, self.student_admin_page.get_page_text())

    def test_13_delete_learners_state_without_correct_unit_id(self):
        '''Delete learners state without correct unit id'''
        self.logger.do_test_name("Delete learners state without correct unit id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_FIRST, variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1 + "1")
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER, self.student_admin_page.get_page_text())

        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER, self.student_admin_page.get_page_text())

    def test_14_show_task_status(self):
        '''Show task status'''
        self.logger.do_test_name("Show task status")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)

        self.student_admin_page.show_task_status(variables.EMPTY, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_STUDENT_EMAIL,
                                      self.student_admin_page.get_page_text())

        self.student_admin_page.show_task_status(variables.LOGIN_EMAIL_INCORRECT, variables.ID_UNIT_1)
        if (variables.VERSION in variables.VERSION_HAWTHORN):
            self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER,
                                          self.student_admin_page.get_page_text())

        self.student_admin_page.show_task_status(variables.LOGIN_EMAIL_FIRST, variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION,
                                      self.student_admin_page.get_page_text())

        self.student_admin_page.show_task_status(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1 + "1")
        self.config.do_assert_false_in(variables.PROMPT_PROBLEM_OVERRIDDEN, self.student_admin_page.get_page_text())
        self.config.do_assert_false_in(variables.TEXT_SUCCESS, self.student_admin_page.get_page_text())

        self.student_admin_page.show_task_status(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.TEXT_SUCCESS, self.student_admin_page.get_page_text())

    def test_15_reset_attempts_for_all_learners(self):
        '''Reset attempts for all learners'''
        self.logger.do_test_name("Reset attempts for all learners")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.reset_all_attempts(variables.ID_UNIT_1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_TRUE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_16_reset_attempts_for_all_learners_without_correct_unit_id(self):
        '''Reset attempts for all learners without correct unit id'''
        self.logger.do_test_name("Reset attempts for all learners without correct unit id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.reset_all_attempts(variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.reset_all_attempts(variables.UNIT_NAME_1 + "1")
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER_COMPLETE, self.student_admin_page.get_page_text())

        self.student_admin_page.reset_all_attempts(variables.UNIT_NAME_1)
        self.student_admin_page.reset_all_attempts(variables.UNIT_NAME_1)
        self.config.do_assert_true_in(variables.PROMPT_MAKE_SURE_PROBLEM_INDENTINIER_COMPLETE, self.student_admin_page.get_page_text())

    def test_17_show_task_status_for_all_learners(self):
        '''Show task status for all learners'''
        self.logger.do_test_name("Show task status for all learners")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_learners_state(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)

        self.student_admin_page.show_all_task_status(variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.show_all_task_status(variables.ID_UNIT_1 + "1")
        self.config.do_assert_false_in(variables.TEXT_SUCCESS, self.student_admin_page.get_page_text())

        self.student_admin_page.show_all_task_status(variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.TEXT_SUCCESS, self.student_admin_page.get_page_text())

    def test_18_rescore_learners_submission(self):
        '''Rescore learners submission'''
        self.logger.do_test_name("Rescore learners submission")
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
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.incorrect_answer_unit(2)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 0/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(2)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_1, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_2, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_learners_submission(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.rescore_learners_submission(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_19_rescore_learners_submission_without_correct_email(self):
        '''Rescore learners submission without correct email'''
        self.logger.do_test_name("Rescore learners submission without correct email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_learners_submission(variables.EMPTY, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_STUDENT_EMAIL, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_learners_submission(variables.LOGIN_EMAIL_INCORRECT, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_USER_DOES_NOT_EXIST, self.student_admin_page.get_page_text())

    def test_20_rescore_learners_submission_without_correct_unit_id(self):
        '''Rescore learners submission without correct unit id'''
        self.logger.do_test_name("Rescore learners submission without correct unit id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_learners_submission(variables.LOGIN_EMAIL_FIRST, variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_learners_submission(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1 + "1")
        self.config.do_assert_true_in(variables.PROMPT_LEARNERS_GRADE_PROBLEM, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_learners_submission(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.rescore_learners_submission(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.course_page.open_course()

    def test_21_rescore_learners_submission_improves(self):
        '''Rescore learners submission only if improves'''
        self.logger.do_test_name("Rescore learners submission only if improves")
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
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.incorrect_answer_unit(2)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 0/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(2)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_1, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_2, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_learners_submission_improves(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.rescore_learners_submission_improves(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_2_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_67, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_22_rescore_learners_submission_improves_without_correct_email(self):
        '''Rescore learners submission improves without correct email'''
        self.logger.do_test_name("Rescore learners submission improves without correct email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_learners_submission_improves(variables.EMPTY, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_STUDENT_EMAIL, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_learners_submission_improves(variables.LOGIN_EMAIL_INCORRECT, variables.ID_UNIT_1)
        self.config.do_assert_true_in(variables.PROMPT_USER_DOES_NOT_EXIST, self.student_admin_page.get_page_text())

    def test_23_rescore_learners_submission_improves_without_correct_unit_id(self):
        '''Rescore learners submission improves without correct unit id'''
        self.logger.do_test_name("Rescore learners submission improves without correct unit id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_learners_submission_improves(variables.LOGIN_EMAIL_FIRST, variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_learners_submission_improves(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1 + "1")
        self.config.do_assert_true_in(variables.PROMPT_LEARNERS_GRADE_PROBLEM, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_learners_submission_improves(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.rescore_learners_submission_improves(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.course_page.open_course()

    def test_24_rescore_all_learners_submission(self):
        '''Rescore all learners submission'''
        self.logger.do_test_name("Rescore all learners submission")
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
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.incorrect_answer_unit(2)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 0/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(2)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_1, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_2, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_all_learners_submission(variables.ID_UNIT_1)
        self.student_admin_page.rescore_all_learners_submission(variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 0/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())

    def test_25_rescore_all_learners_submission_without_correct_unit_id(self):
        '''Rescore all learners submission without correct unit id'''
        self.logger.do_test_name("Rescore all learners submission without correct unit id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_all_learners_submission(variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_all_learners_submission(variables.ID_UNIT_1 + "1")
        self.config.do_assert_true_in(variables.PROMPT_LEARNERS_GRADE_PROBLEM, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_all_learners_submission(variables.ID_UNIT_1)
        self.student_admin_page.rescore_all_learners_submission(variables.ID_UNIT_1)
        self.course_page.open_course()

    def test_26_rescore_all_learners_submission_improves(self):
        '''Rescore all learners submission only if improves'''
        self.logger.do_test_name("Rescore all learners submission only if improves")
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
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.incorrect_answer_unit(2)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 0/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.incorrect_answer_unit(1)
        self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_INCORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.correct_answer_unit(2)
        self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_true_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_1_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 0/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_33, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_1, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.course_outline_page.set_unit_xblock_value(variables.UNIT_NAME_2, variables.FILE_PATH_FIRST_CORRECT_ANSWER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_all_learners_submission_improves(variables.ID_UNIT_1)
        self.student_admin_page.rescore_all_learners_submission_improves(variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_2_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_67, self.progress_page.get_grade_result_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.course_page.select_unit(2)
        if(variables.VERSION in variables.VERSION_GINKO):
            self.config.do_assert_true_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        else:
            self.config.do_assert_false_in(variables.PROMPT_THIS_ANSWER_CORRECT, self.course_page.get_visible_result())
        self.config.do_assert_false_in(variables.TEXT_CORRECT_ANSWER, self.course_page.get_about_unit_text())
        self.config.do_assert_true(variables.STATUS_FALSE, self.course_page.get_activity_submit())
        self.progress_page.open_progress()
        self.config.do_assert_true_in(variables.TEXT_ANSWER_2_OF_3, self.progress_page.get_subsection_result_text())
        self.config.do_assert_true_in("Problem Scores: 1/1 1/1 0/1", self.progress_page.get_subsection_result_text())
        if (variables.PROJECT not in variables.PROJECT_E4H):
            self.config.do_assert_true_in(variables.TEXT_GRADE_67, self.progress_page.get_grade_result_text())

    def test_27_rescore_all_learners_submission_improves_without_correct_unit_id(self):
        '''Rescore all learners submission improves without correct unit id'''
        self.logger.do_test_name("Rescore all learners submission improves without correct unit id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                               variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.rescore_all_learners_submission_improves(variables.EMPTY)
        self.config.do_assert_true_in(variables.PROMPT_PLEASE_ENTER_PROBLEM_LOCATION, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_all_learners_submission_improves(variables.ID_UNIT_1 + "1")
        self.config.do_assert_true_in(variables.PROMPT_LEARNERS_GRADE_PROBLEM, self.student_admin_page.get_page_text())

        self.student_admin_page.rescore_all_learners_submission_improves(variables.ID_UNIT_1)
        self.student_admin_page.rescore_all_learners_submission_improves(variables.ID_UNIT_1)
        self.course_page.open_course()

    def test_28_reimport_courses(self):
        '''Reimport courses'''
        self.logger.do_test_name("Reimport courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
