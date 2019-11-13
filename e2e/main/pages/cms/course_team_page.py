import time
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.logger import Logger
from e2e.main.conf.config import Config
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class CourseTeamPage():

    PATH_COURSE_TEAM_OUTLINE = "//a[contains(text(), 'Course Team')]"
    PATH_ADD_MEMBER_BUTTON = "//a[@class='action action-primary button new-button create-user-button'] | //a[@class='button new-button create-user-button']"
    PATH_NEW_TEAM_MEMBER_BUTTON = "//a[@class='button new-button create-user-button']"
    PATH_EMAIL_FIELD = "//input[@id='user-email-input']"
    PATH_ADD_USER_BUTTON = "//button[contains(text(), 'Add User')]"
    PATH_CANCEL_BUTTON = "//button[contains(text(), 'Cancel')]"
    PATH_COURSE_TEAM_LIST = "//article[@class='content-primary']"
    PATH_OK_BUTTON = "//button[contains(text(), 'Ok')] | //button[contains(text(), 'Return and add email address')]"
    PATH_DELETE_BUTTON = "//button[contains(text(), 'Delete')]"
    PATH_PROMPT_MESSAGE = "//p[@class='message']"

    def __init__(self, driver, *args, **kwargs):
        super(CourseTeamPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)

    def open_course_team(self):
        '''Course Team'''
        self.logger.do_click('Settings')
        self.config.wait_element(self.course_outline_page.PATH_SETTINGS_BUTTON)
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_SETTINGS_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Course Team')
        self.config.wait_element(self.PATH_COURSE_TEAM_OUTLINE)
        self.driver.find_element_by_xpath(self.PATH_COURSE_TEAM_OUTLINE).click()
        time.sleep(3)

    def add_team_member(self, email):
        '''Add new team member'''
        self.logger.do_click('Add new team member')
        self.driver.find_element_by_xpath(self.PATH_ADD_MEMBER_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('Users email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FIELD).send_keys(email)
        time.sleep(1)
        self.logger.do_click('ADD USER')
        self.driver.find_element_by_xpath(self.PATH_ADD_USER_BUTTON).click()
        time.sleep(3)

    def delete_team_member(self, name):
        '''Delete new team member'''
        self.logger.do_click('Sign delete')
        self.driver.find_element_by_xpath("//a[@data-id='" + name + "']").click()
        time.sleep(1)
        self.logger.do_click('Delete')
        self.driver.find_element_by_xpath(self.PATH_DELETE_BUTTON).click()
        time.sleep(3)

    def add_admin_access(self, email):
        '''Add admin access'''
        self.logger.do_click('Add Admin Access')
        self.driver.find_element_by_xpath("//li[@data-email='" + email + "']/ul/li/a").click()
        time.sleep(3)

    def remove_admin_access(self, email):
        '''Add admin access'''
        self.logger.do_click('Add Admin Access')
        self.driver.find_element_by_xpath("//li[@data-email='" + email + "']/ul/li/a").click()
        time.sleep(3)

    def click_ok(self):
        '''Click OK'''
        self.logger.do_click('Ok')
        self.driver.find_element_by_xpath(self.PATH_OK_BUTTON).click()
        time.sleep(1)

    def click_cancel(self):
        '''Click Cancel'''
        self.logger.do_click('Cancel')
        self.driver.find_element_by_xpath(self.PATH_CANCEL_BUTTON).click()
        time.sleep(1)

    def delete_user(self, email):
        '''Delete user'''
        try:
            self.remove_admin_access(email)
        except:
            pass
        try:
            self.delete_team_member(email)
        except:
            pass



    def get_course_team_list(self):
        '''Get users on course team page'''
        return self.driver.find_element_by_xpath(self.PATH_COURSE_TEAM_LIST).text.replace('\n', '; ')

    def get_prompt_message_on_page(self):
        '''Get prompt message on list'''
        return  self.driver.find_element_by_xpath(self.PATH_PROMPT_MESSAGE).text.replace('\n', '; ')

    def get_present_add_team_member_button(self):
        '''Get present add team member button'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_NEW_TEAM_MEMBER_BUTTON).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result