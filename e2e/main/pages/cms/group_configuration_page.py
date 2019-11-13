import random
import time
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class GroupConfigurationPage():

    PATH_GROUPE_CONFIGURATIONS_BUTTON = "//a[contains(text(), 'Group Configurations')]"
    PATH_GROUPE_ADD_BUTTON = "//a[@class='button new-button'] | //button[@class='action action-add ']"

    PATH_GROUP_NAME_FIELD = "//input[@name='group-cohort-name']"
    PATH_CREATE_BUTTON = "//button[contains(text(), 'Create')]"

    def __init__(self, driver, *args, **kwargs):
        super(GroupConfigurationPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.course_outline_page = CourseOutlinePage(self.driver)



    def get_group_name(self):
        '''Get group name'''
        groupName = "Group_#_" + str(random.randint(1, 100000))
        return groupName

    def open_group_configuration(self):
        '''Open group configuration'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_SETTINGS_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Group Configuration')
        self.driver.find_element_by_xpath(self.PATH_GROUPE_CONFIGURATIONS_BUTTON).click()
        time.sleep(3)

    def add_group(self, groupName):
        '''Add group'''
        self.logger.do_click('Add your first content group')
        self.driver.find_element_by_xpath(self.PATH_GROUPE_ADD_BUTTON).click()
        self.logger.do_input('Content Group Name = "' + groupName + '"')
        self.driver.find_element_by_xpath(self.PATH_GROUP_NAME_FIELD).send_keys(groupName)
        self.logger.do_click('Create')
        self.driver.find_element_by_xpath(self.PATH_CREATE_BUTTON).click()
        time.sleep(3)
