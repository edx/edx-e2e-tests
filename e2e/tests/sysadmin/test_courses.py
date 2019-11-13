from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.registration_page import RegistrationPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.tests.main_class import MainClass

class TestCourses(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_05_delete_created_courses
        '''

    def setUp(self):
        super(TestCourses, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.registration_rage = RegistrationPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)

    def test_01_delete_course(self):
        '''Delete course'''
        self.logger.do_test_name("Delete course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_random()
        courseRun = variables.COURSE_RUN
        courseId = variables.ID + organization + "+" + courseNumber + "+" + courseRun
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.config.do_assert_true_in(courseId, self.sysadmin_page.get_courses_list_text())
        self.sysadmin_page.delete_course(courseId)
        self.config.do_assert_false_in(courseId, self.sysadmin_page.get_courses_list_text())

    def test_02_delete_course_by_name(self):
        '''Delete course by name'''
        self.logger.do_test_name("Delete course by name")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_random()
        courseRun = variables.COURSE_RUN
        courseId = variables.ID + organization + "+" + courseNumber + "+" + courseRun
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.config.do_assert_true_in(courseId, self.sysadmin_page.get_courses_list_text())
        self.sysadmin_page.delete_course(courseName)
        self.config.do_assert_true_in(courseId, self.sysadmin_page.get_courses_list_text())
        self.sysadmin_page.delete_course(courseId)
        self.config.do_assert_false_in(courseId, self.sysadmin_page.get_courses_list_text())

    def test_03_twice_delete_course(self):
        '''Twice delete course'''
        self.logger.do_test_name("Twice delete course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_random()
        courseRun = variables.COURSE_RUN
        courseId = variables.ID + organization + "+" + courseNumber + "+" + courseRun
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.config.do_assert_true_in(courseId, self.sysadmin_page.get_courses_list_text())
        self.sysadmin_page.delete_course(courseId)
        self.sysadmin_page.delete_course(courseId)
        self.config.do_assert_false_in(courseId, self.sysadmin_page.get_courses_list_text())

    def test_04_delete_course_with_incorrect_id(self):
        '''Delete course with incorrect id'''
        self.logger.do_test_name("Delete course with incorrect id")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        courseName = variables.COURSE_NAME
        organization = variables.ORGANIZATION_FOR_DELETE
        courseNumber = self.config.get_random()
        courseRun = variables.COURSE_RUN
        courseId = variables.ID + organization + "+" + courseNumber + "+" + courseRun
        courseIdIncorrect = variables.ID + organization + "+" + courseNumber + "+" + courseRun + "1"
        self.course_outline_page.create_course(courseName, organization, courseNumber, courseRun)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.config.do_assert_true_in(courseId, self.sysadmin_page.get_courses_list_text())
        self.sysadmin_page.delete_course(courseIdIncorrect)
        self.config.do_assert_true_in(courseId, self.sysadmin_page.get_courses_list_text())
        self.sysadmin_page.delete_course(courseId)
        self.config.do_assert_false_in(courseId, self.sysadmin_page.get_courses_list_text())

    def test_05_delete_created_courses(self):
        '''Deleting all created courses'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.sysadmin_page.delete_created_courses()