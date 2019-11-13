from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.home_page import HomePage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.cms.pages_page import PagesPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.tests.main_class import MainClass

class TestPagesVisibility(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_06_reimport_courses
        '''

    def setUp(self):
        super(TestPagesVisibility, self).setUp()
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

    def test_01_main_pages_doesnt_delete(self):
        '''Unit visible all positive'''
        self.logger.do_test_name("Unit visible all positive")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.pages_page.open_pages()
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_edit_page())
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_delete_page())

    def test_02_add_new_page(self):
        '''Add new page'''
        self.logger.do_test_name("Add new page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.pages_page.open_pages()
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_edit_page())
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_delete_page())
        self.pages_page.add_page()
        self.config.do_assert_true(variables.STATUS_ON, self.pages_page.get_possible_edit_page())
        self.config.do_assert_true(variables.STATUS_ON, self.pages_page.get_possible_delete_page())
        pagesName = variables.PAGES_NAME
        self.pages_page.change_page(pagesName)
        self.config.do_assert_true_in(variables.PAGES_NAME, self.pages_page.get_pages_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.config.do_assert_false_in(variables.PAGES_DEFOULT_NAME, self.course_page.get_all_course_information_text())
        self.pages_page.open_new_page(pagesName)
        self.config.do_assert_true(variables.PROMPT_PAGES_TEXT, self.pages_page.get_pages_text())

    def test_03_delete_new_page(self):
        '''Delete new page'''
        self.logger.do_test_name("Delete new page")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.pages_page.open_pages()
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_edit_page())
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_delete_page())
        self.pages_page.add_page()
        self.config.do_assert_true(variables.STATUS_ON, self.pages_page.get_possible_edit_page())
        self.config.do_assert_true(variables.STATUS_ON, self.pages_page.get_possible_delete_page())
        self.config.do_assert_true_in(variables.PAGES_DEFOULT_NAME, self.pages_page.get_pages_list())
        self.pages_page.delete_page()
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_edit_page())
        self.config.do_assert_true(variables.STATUS_OFF, self.pages_page.get_possible_delete_page())
        self.config.do_assert_false_in(variables.PAGES_DEFOULT_NAME, self.pages_page.get_pages_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.config.do_assert_false_in(variables.PAGES_DEFOULT_NAME, self.course_page.get_all_course_information_text())

    def test_04_page_doesnt_visible(self):
        '''Page doesn't visible'''
        self.logger.do_test_name("Page doesn't visible")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.pages_page.open_pages()
        if(variables.PROJECT in variables.PROJECT_ASUOSPP):
            self.pages_page.set_page_unvisible(variables.PAGE_DISCUSSION)
        self.pages_page.set_page_unvisible(variables.PAGE_WIKI)
        self.pages_page.set_page_unvisible(variables.PAGE_PROGRESS)
        self.config.do_assert_true_in(variables.PAGE_HOME, self.pages_page.get_pages_list())
        self.config.do_assert_true_in(variables.PAGE_COURSE, self.pages_page.get_pages_list())
        self.config.do_assert_true_in(variables.PAGE_DISCUSSION, self.pages_page.get_pages_list())
        self.config.do_assert_true_in(variables.PAGE_WIKI, self.pages_page.get_pages_list())
        self.config.do_assert_true_in(variables.PAGE_PROGRESS, self.pages_page.get_pages_list())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.config.do_assert_true_in(variables.PAGE_COURSE, self.course_page.get_all_course_information_text())
        if (variables.PROJECT in variables.PROJECT_ASUOSPP):
            self.config.do_assert_false_in(variables.PAGE_DISCUSSION, self.course_page.get_all_course_information_text())
        else:
            self.config.do_assert_true_in(variables.PAGE_DISCUSSION, self.course_page.get_all_course_information_text())
        self.config.do_assert_false_in(variables.PAGE_WIKI, self.course_page.get_all_course_information_text())
        self.config.do_assert_false_in(variables.PAGE_PROGRESS, self.course_page.get_all_course_information_text())

    def test_05_change_pages_plase(self):
        '''Change pages plase'''
        self.logger.do_test_name("Change pages plase")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.pages_page.open_pages()
        locationDiscussion = self.pages_page.get_pages_location(variables.PAGE_DISCUSSION)
        hightDiscussion = locationDiscussion['y']
        locationProgress = self.pages_page.get_pages_location(variables.PAGE_PROGRESS)
        hightProgress = locationProgress['y']
        self.config.do_assert_more(hightProgress, hightDiscussion)

        self.pages_page.change_pages_plase(variables.PAGE_PROGRESS,
                                           variables.PAGE_DISCUSSION)
        locationDiscussion = self.pages_page.get_pages_location(variables.PAGE_DISCUSSION)
        hightDiscussion = locationDiscussion['y']
        locationProgress = self.pages_page.get_pages_location(variables.PAGE_PROGRESS)
        hightProgress = locationProgress['y']
        self.config.do_assert_more(hightDiscussion, hightProgress)

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        locationDiscussion = self.pages_page.get_pages_location(variables.PAGE_DISCUSSION)
        hightDiscussion = locationDiscussion['x']
        locationProgress = self.pages_page.get_pages_location(variables.PAGE_PROGRESS)
        hightProgress = locationProgress['x']
        self.config.do_assert_more(hightDiscussion, hightProgress)

    def test_06_reimport_courses(self):
        '''Reimport courses'''
        self.logger.do_test_name("Reimport courses")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.home_page.open_home()
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_NEGATIVE, variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)