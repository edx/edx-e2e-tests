import unittest
from e2e.main.pages.login_page import *
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.tests.main_class import MainClass
from e2e.main.pages.lms.instructor.cohorts_page import CohortsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.group_configuration_page import GroupConfigurationPage

class TestCohorts(MainClass):
    '''
        Pre-condition: Absent
        Past-condition: Absent
        '''

    def setUp(self):
        super(TestCohorts, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.cohorts_page = CohortsPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.group_configuration_page = GroupConfigurationPage(self.driver)

    def test_01_enabling_cohorts(self):
        '''Checking enabling instructor'''
        self.logger.do_test_name("Checking enabling instructor")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        self.config.do_assert_true(variables.STATUS_ON, self.cohorts_page.get_possible_add_cohorts())
        self.cohorts_page.setCohortsOff()
        self.config.do_assert_true(variables.STATUS_OFF, self.cohorts_page.get_possible_add_cohorts())

    def test_02_adding_cohorts(self):
        '''Checking adding instructor'''
        self.logger.do_test_name("Checking adding instructor")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        cohortName = self.cohorts_page.getCohortName()
        self.cohorts_page.addCohort(cohortName)
        self.config.do_assert_true_in(cohortName, self.cohorts_page.get_cohorts_compound())

    def test_03_assign_learners_cohorts_manually(self):
        '''Assign Learners to Cohorts Manually'''
        self.logger.do_test_name("Assign Learners to Cohorts Manually")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        cohortName = self.cohorts_page.getCohortName()
        self.cohorts_page.addCohort(cohortName)
        self.config.do_assert_true_in(cohortName + "(0)", self.cohorts_page.get_cohorts_compound())
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(cohortName + "(1)", self.cohorts_page.get_cohorts_compound())
        self.config.do_assert_true_in(cohortName, self.cohorts_page.get_prompt_cohort_contains_student())
        self.config.do_assert_true_in(variables.COHORT_CONTAINS_STUDENT, self.cohorts_page.get_prompt_cohort_contains_student())

    def test_04_change_student_cohort_assignments(self):
        '''Change Student Cohort Assignments'''
        self.logger.do_test_name("Change Student Cohort Assignments")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        cohortNameFirst = self.cohorts_page.getCohortName()
        self.cohorts_page.addCohort(cohortNameFirst)
        self.config.do_assert_true_in(cohortNameFirst + "(0)", self.cohorts_page.get_cohorts_compound())
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(cohortNameFirst + "(1)", self.cohorts_page.get_cohorts_compound())
        self.config.do_assert_true_in(cohortNameFirst, self.cohorts_page.get_prompt_cohort_contains_student())
        self.config.do_assert_true_in(variables.COHORT_CONTAINS_STUDENT, self.cohorts_page.get_prompt_cohort_contains_student())
        cohortNameSecond = self.cohorts_page.getCohortName()
        self.cohorts_page.addCohort(cohortNameSecond)
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(cohortNameFirst + "(0)", self.cohorts_page.get_cohorts_compound())
        self.config.do_assert_true_in(cohortNameSecond + "(1)", self.cohorts_page.get_cohorts_compound())
        self.config.do_assert_true_in(cohortNameSecond, self.cohorts_page.get_prompt_cohort_contains_student())
        self.config.do_assert_true_in(variables.COHORT_CONTAINS_STUDENT, self.cohorts_page.get_prompt_cohort_contains_student())

    @unittest.skipIf(variables.PROJECT == variables.PROJECT_ASUOSPP, "Test doesn't work for ASU OSPP")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_GREEN_HOST, "Test doesn't work for Green Host")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_WARDY, "Test doesn't work for Wardy It")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_GIJIMA, "Test doesn't work for Gijima")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_TBS, "Test doesn't work for Toulouse BS")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_E4H, "Test doesn't work for E4H")
    @unittest.skipIf(variables.PROJECT == variables.PROJECT_SPECTRUM, "Test doesn't work for Spectrum")
    def test_05_create_content_group(self):
        '''Create content group'''
        self.logger.do_test_name("Create content group")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.group_configuration_page.open_group_configuration()
        groupName = self.group_configuration_page.get_group_name()
        self.group_configuration_page.add_group(groupName)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.cohorts_page.openCohorts()
        self.cohorts_page.setCohortsOn()
        cohortName = self.cohorts_page.getCohortName()
        self.cohorts_page.addCohort(cohortName)
        self.config.do_assert_true_in(cohortName + "(0)", self.cohorts_page.get_cohorts_compound())
        self.cohorts_page.assignLearnersCohortsManually(variables.LOGIN_EMAIL_FIRST)
        self.config.do_assert_true_in(cohortName + "(1)", self.cohorts_page.get_cohorts_compound())
        self.config.do_assert_true_in(cohortName, self.cohorts_page.get_prompt_cohort_contains_student())
        self.config.do_assert_true_in(variables.COHORT_CONTAINS_STUDENT, self.cohorts_page.get_prompt_cohort_contains_student())
        self.cohorts_page.add_content_group(groupName)
        self.config.do_assert_true(variables.SAVED_COHORT, self.cohorts_page.get_prompt_saved_cohort())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_outline_page.set_content_group(groupName)
        self.config.do_assert_true_in(groupName, self.course_outline_page.get_courses_groups_text())