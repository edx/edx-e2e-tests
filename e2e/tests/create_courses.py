from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.tests.main_class import MainClass
from e2e.tests.instructor.test_cohorts import variables

class CreateCourse(MainClass):

    def setUp(self):
        super(CreateCourse, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.import_page = ImportPage(self.driver)
        self.home_page = HomePage(self.driver)

    def test_01_create_course(self):
        '''Create courses and enroll learners'''
        self.logger.do_test_name("Create courses and enroll learners")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.create_course(variables.COURSE_NAME, variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)

        self.home_page.open_home()
        self.course_outline_page.create_course(variables.COURSE_NAME, variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_ENROLL, False, False)
        self.dashboard_page.open_dashboard()
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_FIRST, "1", variables.STATUS_ENROLL, False, False)
        self.membership_page.enroll_user(variables.LOGIN_EMAIL_SECOND, "1", variables.STATUS_ENROLL, False, False)