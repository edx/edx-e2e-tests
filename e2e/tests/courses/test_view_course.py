import time
import unittest
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.group_configuration_page import GroupConfigurationPage
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.cms.pages_page import PagesPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.lms.instructor.cohorts_page import CohortsPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.lms.instructor.student_admin_page import StudentAdminPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.tests.main_class import MainClass

class TestViewCourse(MainClass):
    '''
        Pre-condition:
            test_00_import_courses
        Past-condition:
            test_08_reimport_courses
        '''

    def setUp(self):
        super(TestViewCourse, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.pages_page = PagesPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.course_page = CoursePage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.import_page = ImportPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.student_admin_page = StudentAdminPage(self.driver)
        self.cohorts_page = CohortsPage(self.driver)
        self.group_configuration_page = GroupConfigurationPage(self.driver)

    def test_00_import_courses(self):
        '''Import courses'''
        self.logger.do_test_name("Import courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)

    def test_01_view_course_as_staff(self):
        '''View course as staff'''
        self.logger.do_test_name("View course as staff")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.set_view_this_course(variables.STATUS_STAFF, None)
        self.config.do_assert_true_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.TEXT_SUBMISSION_HISTORY, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_STAFF_DEBUG_INFO, self.course_page.get_about_unit_text())

    def test_02_view_course_as_learner(self):
        '''View course as learner'''
        self.logger.do_test_name("View course as learner")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.set_view_this_course(variables.STATUS_LEARNER, None)
        self.config.do_assert_false_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_SUBMISSION_HISTORY, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_STAFF_DEBUG_INFO, self.course_page.get_about_unit_text())

    def test_03_view_course_as_specific_learner_by_email(self):
        '''View course as Specific learner by email'''
        self.logger.do_test_name("View course as Specific learner by email")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.course_page.incorrect_answer_unit(2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.set_view_this_course(variables.STATUS_SPECIFIC_LEARNER, variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_false_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.config.do_assert_true_in('You are now viewing the course as ' + variables.NAME_FIRST, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.TEXT_SUBMISSION_HISTORY, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_STAFF_DEBUG_INFO, self.course_page.get_about_unit_text())

        self.course_page.select_unit(1)
        self.config.do_assert_true(variables.STATUS_CORRECT, self.course_page.get_visible_correct_result())
        self.config.do_assert_false(variables.STATUS_INCORRECT, self.course_page.get_visible_correct_result())
        self.course_page.select_unit(2)
        self.config.do_assert_false(variables.STATUS_CORRECT, self.course_page.get_visible_correct_result())
        self.config.do_assert_true(variables.STATUS_INCORRECT, self.course_page.get_visible_correct_result())

    def test_04_view_course_as_specific_learner_by_name(self):
        '''View course as Specific learner by name'''
        self.logger.do_test_name("View course as Specific learner by name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.course_page.incorrect_answer_unit(2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.set_view_this_course(variables.STATUS_SPECIFIC_LEARNER, variables.NAME_FIRST)
        self.config.do_assert_false_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.config.do_assert_true_in('You are now viewing the course as ' + variables.NAME_FIRST, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.course_page.open_course()
        self.course_page.open_unit()
        self.config.do_assert_true_in(variables.TEXT_SUBMISSION_HISTORY, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_STAFF_DEBUG_INFO, self.course_page.get_about_unit_text())

        self.course_page.select_unit(1)
        self.config.do_assert_true(variables.STATUS_CORRECT, self.course_page.get_visible_correct_result())
        self.config.do_assert_false(variables.STATUS_INCORRECT, self.course_page.get_visible_correct_result())
        self.course_page.select_unit(2)
        self.config.do_assert_false(variables.STATUS_CORRECT, self.course_page.get_visible_correct_result())
        self.config.do_assert_true(variables.STATUS_INCORRECT, self.course_page.get_visible_correct_result())

    def test_05_view_course_as_specific_learner_by_empty_email(self):
        '''View course as Specific learner by empty email'''
        self.logger.do_test_name("View course as Specific learner by empty email ")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.set_view_this_course(variables.STATUS_SPECIFIC_LEARNER, variables.EMPTY)
        self.config.do_assert_true_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.config.do_assert_false_in('You are now viewing the course as ' + variables.NAME_FIRST, self.course_page.get_top_course_information_text(variables.STATUS_ON))

    def test_06_view_course_as_specific_learner_by_incorrect_email(self):
        '''View course as Specific learner by empty email'''
        self.logger.do_test_name("View course as Specific learner by empty email ")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.set_view_this_course(variables.STATUS_SPECIFIC_LEARNER, variables.LOGIN_EMAIL_INCORRECT)
        self.config.do_assert_true_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.config.do_assert_false_in('You are now viewing the course as ' + variables.NAME_FIRST, self.course_page.get_top_course_information_text(variables.STATUS_ON))

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_07_view_course_as_specific_learner_by_cohort(self):
        '''View course as Specific learner by cohort'''
        self.logger.do_test_name("View course as Specific learner by cohort ")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.group_configuration_page.open_group_configuration()
        groupNameFirst = self.group_configuration_page.get_group_name()
        groupNameSecond = self.group_configuration_page.get_group_name()
        self.group_configuration_page.add_group(groupNameFirst)
        self.group_configuration_page.add_group(groupNameSecond)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_SECOND, variables.ID_UNIT_2)
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        self.cohorts_page.select_cohort(variables.PATH_EXTRA_COHORT)
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_FIRST)
        self.cohorts_page.add_content_group(groupNameFirst)
        self.cohorts_page.select_cohort(variables.PATH_DEFOLT_COHORT)
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_SECOND)
        self.cohorts_page.add_content_group(groupNameSecond)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.course_outline_page.set_content_group(groupNameSecond)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_page.open_course()
        time.sleep(15)
        self.config.refresh_page()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_IRONWOOD):
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
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_SECOND, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.correct_answer_unit(1)
        self.course_page.incorrect_answer_unit(2)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.set_view_this_course("Learner in " + groupNameFirst, None)
        self.config.do_assert_false_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text())
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_IRONWOOD):
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

        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_SUBMISSION_HISTORY, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_STAFF_DEBUG_INFO, self.course_page.get_about_unit_text())

        self.course_page.set_view_this_course("Learner in " + groupNameSecond, None)
        self.config.do_assert_false_in(variables.PAGES_INSTRUCTOR, self.course_page.get_top_course_information_text(variables.STATUS_ON))
        self.course_page.open_course()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_unit_list_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_unit_list_text())
        if (variables.VERSION in variables.VERSION_HAWTHORN + variables.VERSION_IRONWOOD):
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_unit_list_text())
            self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_unit_list_text())
            self.course_page.open_unit()
            self.course_page.select_unit(1)
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_GINKO):
            self.course_page.open_subsection()
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())
        elif (variables.VERSION in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
            self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())
        else:
            print("Incorrect Project")
            self.config.do_assert_true(1, 2)

        self.course_page.open_unit()
        self.config.do_assert_false_in(variables.TEXT_SUBMISSION_HISTORY, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_STAFF_DEBUG_INFO, self.course_page.get_about_unit_text())

    def test_08_reimport_courses(self):
        '''Reimport courses'''
        self.logger.do_test_name("Reimport courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)