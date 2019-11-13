from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.course_team_page import CourseTeamPage
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.tests.main_class import MainClass
from e2e.tests.instructor.test_cohorts import variables

class DeleteAllChanges(MainClass):

    def setUp(self):
        super(DeleteAllChanges, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.course_team_page = CourseTeamPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.membership_page = MembershipPage(self.driver)

    def test_01_delete_created_courses(self):
        '''Deleting all created courses'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_courses()
        self.sysadmin_page.delete_created_courses()

    def test_02_set_ended_dates_of_course(self):
        '''Set ended dates of course'''
        self.logger.do_test_name('Set ended dates of course')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_NONE)

    def test_03_delete_roles(self):
        '''Delete roles'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())

        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())

        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.course_team_page.open_course_team()
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_FIRST)
        self.course_team_page.delete_user(variables.LOGIN_EMAIL_SECOND)
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_FIRST, self.course_team_page.get_course_team_list())
        self.config.do_assert_false_in(variables.LOGIN_EMAIL_SECOND, self.course_team_page.get_course_team_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.dashboard_page.open_cours()
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()

        self.dashboard_page.open_dashboard()
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()

        self.dashboard_page.open_dashboard()
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.membership_page.open_membership()
        self.membership_page.delete_all_roles()