from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.lms.instructor.open_responses_page import OpenResponsesPage
from e2e.main.pages.lms.progress_page import ProgressPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.tests.main_class import MainClass
from e2e.tests.instructor.test_cohorts import variables

class TestBookmarks(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_05_reimport_courses
        '''

    def setUp(self):
        super(TestBookmarks, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.course_page = CoursePage(self.driver)
        self.progress_page = ProgressPage(self.driver)
        self.open_responses_page = OpenResponsesPage(self.driver)
        self.import_page = ImportPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.home_page = HomePage(self.driver)

    def test_01_add_bookmark(self):
        '''Add bookmark'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_course_number()
        courseRun = variables.COURSE_RUN
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_2, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.config.do_assert_true_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())

        self.course_page.bookmark_unit(variables.STATUS_ON)
        self.config.do_assert_false_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())

        self.course_page.open_course()
        self.course_page.open_bookmarks()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())

        self.course_page.click_view_unit()
        self.config.do_assert_true_in(variables.BLOCK_MULTIPLE_CHOICE, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())

    def test_02_delete_bookmark(self):
        '''Delete bookmark'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_course_number()
        courseRun = variables.COURSE_RUN
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_2, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.config.do_assert_true_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())
        self.course_page.select_unit(2)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.config.do_assert_true_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())

        self.course_page.select_unit(1)
        self.course_page.bookmark_unit(variables.STATUS_ON)
        self.config.do_assert_false_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())
        self.course_page.select_unit(2)
        self.course_page.bookmark_unit(variables.STATUS_ON)
        self.config.do_assert_false_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())

        self.course_page.select_unit(1)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.config.do_assert_true_in(variables.TEXT_BOOKMARK, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.TEXT_BOOKMARKED, self.course_page.get_about_unit_text())

        self.course_page.open_course()
        self.course_page.open_bookmarks()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())

    def test_03_rename_unit_in_bookmarks(self):
        '''Rename unit in bookmarks'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_course_number()
        courseRun = variables.COURSE_RUN
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_2, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.course_page.bookmark_unit(variables.STATUS_ON)
        self.course_page.select_unit(2)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.course_page.bookmark_unit(variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(organization, courseNumber, courseRun)
        self.course_outline_page.rename_unit(variables.UNIT_NAME_1, variables.UNIT_NAME_5)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.course_page.open_bookmarks()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_5, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())

    def test_04_delete_unit_in_bookmarks(self):
        '''Delete unit in bookmarks'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_course_number()
        courseRun = variables.COURSE_RUN
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.course_outline_page.add_section(variables.SECTION_NAME_1)
        self.course_outline_page.add_subsection(variables.SUBSECTION_NAME_1)
        self.course_outline_page.add_unit(variables.UNIT_NAME_1, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.course_outline_page.add_unit(variables.UNIT_NAME_2, variables.EMPTY,
                                          variables.BLOCK_MULTIPLE_CHOICE)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.course_page.open_unit()
        self.course_page.select_unit(1)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.course_page.bookmark_unit(variables.STATUS_ON)
        self.course_page.select_unit(2)
        self.course_page.bookmark_unit(variables.STATUS_OFF)
        self.course_page.bookmark_unit(variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(organization, courseNumber, courseRun)
        self.course_outline_page.delete_unit()
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_course(organization, courseNumber, courseRun)
        self.course_page.open_course()
        self.course_page.open_bookmarks()
        self.config.do_assert_true_in(variables.SECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.SUBSECTION_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_false_in(variables.UNIT_NAME_1, self.course_page.get_about_unit_text())
        self.config.do_assert_true_in(variables.UNIT_NAME_2, self.course_page.get_about_unit_text())

    def test_05_delete_created_courses(self):
        '''Delete created courses'''
        self.logger.do_test_name("Delete created courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.sysadmin_page.delete_created_courses()


