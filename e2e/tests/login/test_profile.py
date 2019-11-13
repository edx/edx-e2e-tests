import unittest
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.account_page import AccountPage
from e2e.main.pages.lms.courses_page import CoursesPage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.lms.profile_page import ProfilePage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.tests.main_class import MainClass


class TestProfile(MainClass):
    '''
        Pre-condition: Absent
        Past-condition: Absent
        '''

    def setUp(self):
        super(TestProfile, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.profile_page = ProfilePage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.account_page = AccountPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.courses_page = CoursesPage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        # suite working 18m

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_01_set_profile_visibility(self):
        '''Set profile visibility'''
        self.logger.do_test_name("Set profile visibility")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.profile_page.input_location(variables.AUSTRIA)
        self.profile_page.input_language(variables.LANGUAGE_ALBANIAN)
        self.profile_page.input_about_me(variables.TEXT_SOME_TEXT)

        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.TEXT_EXPLORE_NEW_COURSES, self.profile_page.get_profile_text())

        self.profile_page.set_profile_visibility(variables.LIMITED_PROFILE)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.PROJECT not in (variables.PROJECT_GIJIMA + variables.PROJECT_WARDY + variables.PROJECT_SPECTRUM)):
            self.config.do_assert_false_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        if (variables.PROJECT not in (variables.PROJECT_GIJIMA + variables.PROJECT_WARDY + variables.PROJECT_SPECTRUM + variables.PROJECT_LETSTUDY)):
            self.config.do_assert_false_in(variables.TEXT_EXPLORE_NEW_COURSES, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_02_profile_visibility_for_young(self):
        '''Profile visibility for young'''
        self.logger.do_test_name("Profile visibility for young")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_YOUNG)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.config.do_assert_true(variables.STATUS_TRUE, self.profile_page.get_activity_profilele_disabled())
        self.config.do_assert_true(variables.STATUS_OFF, self.profile_page.get_possible_change_profile_visibility(variables.FULL_PROFILE))
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.config.do_assert_true_in(variables.STATUS_NONE, self.profile_page.get_activity_profilele_disabled())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_03_change_location(self):
        '''Chacking changing location'''
        self.logger.do_test_name("Chacking changing location")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.profile_page.input_location(variables.AUSTRIA)
        self.config.do_assert_true_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.AUSTRIA_SHORT, self.account_page.get_region())
        self.profile_page.open_profile()
        self.profile_page.input_location(variables.ARUBA)
        self.config.do_assert_false_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.ARUBA, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.ARUBA_SHORT, self.account_page.get_region())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_04_change_language(self):
        '''Chacking changing language'''
        self.logger.do_test_name("Chacking changing language")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.profile_page.input_language(variables.LANGUAGE_ALBANIAN)
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN_SHORT, self.account_page.get_preferred_language())
        self.profile_page.open_profile()
        self.profile_page.input_language(variables.LANGUAGE_ARABIC)
        self.config.do_assert_false_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.LANGUAGE_ARABIC, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.config.do_assert_true_in(variables.LANGUAGE_ARABIC_SHORT, self.account_page.get_preferred_language())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_05_change_about_me(self):
        '''Chacking changing about me'''
        self.logger.do_test_name("Chacking changing about me")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.profile_page.input_about_me(variables.TEXT_SOME_TEXT)
        self.config.do_assert_true_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        self.profile_page.input_about_me(variables.TEXT_SOME_NEW_TEXT)
        self.config.do_assert_false_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_NEW_TEXT, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.profile_page.input_about_me(variables.LENGTH_FIELD_301)
            self.config.do_assert_false_in(variables.LENGTH_FIELD_301, self.profile_page.get_profile_text())
            self.config.do_assert_true_in(variables.LENGTH_FIELD_300, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_06_disable_values_for_change_limited_profile(self):
        '''Disable values for change limited profile'''
        self.logger.do_test_name("Disable values for change limited profile")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.profile_page.input_location(variables.AUSTRIA)
        self.profile_page.input_language(variables.LANGUAGE_ALBANIAN)
        self.profile_page.input_about_me(variables.TEXT_SOME_TEXT)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        self.profile_page.set_profile_visibility(variables.LIMITED_PROFILE)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_false_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_07_disable_values_for_change_young_age(self):
        '''Disable values for change young age'''
        self.logger.do_test_name("Disable values for change young age")
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.profile_page.input_location(variables.AUSTRIA)
        self.profile_page.input_language(variables.LANGUAGE_ALBANIAN)
        self.profile_page.input_about_me(variables.TEXT_SOME_TEXT)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_YOUNG)
        self.profile_page.open_profile()
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_false_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_false_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())
        self.config.do_assert_true(variables.STATUS_TRUE, self.profile_page.get_activity_profilele_disabled())
        self.config.do_assert_true(variables.STATUS_OFF,
                                   self.profile_page.get_possible_change_profile_visibility(variables.FULL_PROFILE))
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.set_profile_visibility(variables.FULL_PROFILE)
        self.config.do_assert_true_in(variables.NAME_FIRST, self.profile_page.get_profile_text())
        if (variables.VERSION not in variables.VERSION_FIKUS):
            self.config.do_assert_true_in(variables.FULL_NAME, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.AUSTRIA, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.LANGUAGE_ALBANIAN, self.profile_page.get_profile_text())
        self.config.do_assert_true_in(variables.TEXT_SOME_TEXT, self.profile_page.get_profile_text())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_08_search_some_course(self):
        '''Soearch some course'''
        self.logger.do_test_name("Soearch some course")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_AFTER_TODAY_01)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_BOTH)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.profile_page.open_profile()
        self.profile_page.click_explore_new_courses()
        self.courses_page.scroll_oll_page()
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.courses_page.get_courses_list_text())
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_NONE)

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_09_change_twitter_link(self):
        '''Checking changing twitter link'''
        self.logger.do_test_name("Checking changing twitter link")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE,
                                    variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER,
                              variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.account_page.input_twitter(variables.URL_TWITTER_PROFILE)
        self.profile_page.open_profile()
        self.profile_page.open_twitter_profile()
        self.config.switch_window(1)
        self.config.do_assert_true_in(variables.LOG_IN, self.profile_page.get_twitter_profile_present())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_10_change_facebook_link(self):
        '''Checking changing facebook link'''
        self.logger.do_test_name("Checking changing facebook link")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE,
                                    variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER,
                              variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.account_page.input_facebook(variables.URL_FACEBOOK_PROFILE)
        self.profile_page.open_profile()
        self.profile_page.open_facebook_profile()
        self.config.switch_window(1)
        self.config.do_assert_true_in(variables.LOG_IN, self.profile_page.get_facebook_profile_present())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    @unittest.skipIf(variables.VERSION == variables.VERSION_FIKUS, "Test doesn't work for Fikus")
    def test_11_change_linkedin_link(self):
        '''Checking changing linkedin link'''
        self.logger.do_test_name("Checking changing linkedin link")
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.sysadmin_page.open_users()
        self.sysadmin_page.delete_user(variables.LOGIN_EMAIL_CREATED_USER)
        self.sysadmin_page.add_user(variables.LOGIN_EMAIL_CREATED_USER, variables.NAME_FOR_CREATE,
                                    variables.LOGIN_PASSWORD_CREATED_USER)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_CREATED_USER, variables.LOGIN_PASSWORD_CREATED_USER,
                              variables.STATUS_LMS)
        self.login_page.set_leng(variables.LOGIN_EMAIL_CREATED_USER, variables.STATUS_LMS)
        self.account_page.open_account()
        self.account_page.input_age(variables.YEAR_2000)
        self.account_page.input_linkedin(variables.URL_LINKEDIN_PROFILE)
        self.profile_page.open_profile()
        self.profile_page.open_linkedin_profile()
        self.config.switch_window(1)
        self.config.do_assert_true_in(variables.SIGN_IN, self.profile_page.get_linkedin_profile_present())

    @unittest.skipIf(variables.VERSION == variables.VERSION_GINKO, "Test doesn't work for Ginko")
    def test_12_set_ended_dates_of_course(self):
        '''Set ended dates of course'''
        self.logger.do_test_name('Set ended dates of course')
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_course()
        self.shedule_details_page.open_shedule_details()
        self.shedule_details_page.input_date(variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02,
                                             variables.DATE_BEFORE_TODAY_01, variables.DATE_BEFORE_TODAY_02)
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CATALOG_VISIBILITY, variables.STATUS_VISIBILITY_NONE)