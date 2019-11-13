import random
import time
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables
from e2e.main.conf.config import Config

class CohortsPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_COHORTS_BUTTON = "//button[contains(text(), 'Cohorts')]"
    PATH_ENABLE_COHORTS_BUTTON = "//div[@class='cohorts-state-section']/label/input"
    PATH_ADD_COHORTS_BUTTON = "//button[@class='action-primary action-create'] | //button[@class='button action-primary action-create']"
    PATH_COHORT_NAME_FIELD = "//input[@id='cohort-name']"
    PATH_SAVE_BUTTON = "//button[@class='form-submit button action-primary action-save']"
    PATH_COHORTS_FIELD = "//select[@class='input cohort-select']"

    PATH_MANAGE_STUDENTS_BUTTON = "//button[contains(text(), 'Manage Students')] | //button[contains(text(), 'Manage Learners')]"
    PATH_SETTINGS_BUTTON = "//button[contains(text(), 'Settings')]"
    PATH_SELECT_CONTENT_GROUP_BUTTON = "//div[@class='input-group has-other-input-text']/label"
    PATH_CONTENT_GROUP_NAME_FIELD = "//select[@name='cohort-group-association']"

    PATH_STUDENT_EMAIL_PASSWORD = "//textarea[@id='cohort-management-group-add-students']"
    PATH_ADD_STUDENTS_BUTTON = "//button[@class='form-submit button action-primary action-view']"

    PATH_PROMPT_COHORT_CONTAINS_STUDENT = "//h3[@class='hd hd-3 group-header-title']"
    PATH_PROMPT_SAVED_COHORT = "//div[@class='cohort-management-settings']/form/div/div/h3"

    def __init__(self, driver, *args, **kwargs):
        super(CohortsPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)

    def getCohortName(self):
        '''Get cohorts name'''
        return "Cohort_#_" + str(random.randint(1, 100000))

    def openCohorts(self):
        '''Open cohorts'''
        self.logger.do_click('Instructor')
        self.driver.find_element_by_xpath(self.PATH_INSTRUCTOR_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Cohorts')
        self.driver.find_element_by_xpath(self.PATH_COHORTS_BUTTON).click()
        time.sleep(5)

    def setCohortsOn(self):
        '''Set cohorts on'''
        if(variables.STATUS_TRUE != self.get_cohorts_status()):
            self.logger.do_click('Enable Cohorts')
            self.driver.find_element_by_xpath(self.PATH_ENABLE_COHORTS_BUTTON).click()
            time.sleep(3)
        else:
            self.logger.do_click('Not divided')
            self.driver.find_element_by_xpath(self.PATH_ENABLE_COHORTS_BUTTON).click()
            self.driver.find_element_by_xpath(self.PATH_ENABLE_COHORTS_BUTTON).click()
            time.sleep(3)

    def setCohortsOff(self):
        '''Set cohorts off'''
        if(variables.STATUS_TRUE==self.get_cohorts_status()):
            self.logger.do_click('Enable Cohorts')
            self.driver.find_element_by_xpath(self.PATH_ENABLE_COHORTS_BUTTON).click()
            time.sleep(1)

    def addCohort(self, cohortName):
        '''Add cohorts'''
        self.logger.do_click('Add Cohorts')
        self.config.execute_script_click(self.PATH_ADD_COHORTS_BUTTON)
        time.sleep(1)
        self.logger.do_input('Cohort name = ' + cohortName)
        self.driver.find_element_by_xpath(self.PATH_COHORT_NAME_FIELD).send_keys(cohortName)
        self.logger.do_click('Save')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(3)

    def openManageStudents(self):
        '''Open Manage Students'''
        self.logger.do_click('Manage Students')
        self.driver.find_element_by_xpath(self.PATH_MANAGE_STUDENTS_BUTTON).click()

    def openSettings(self):
        '''Open Settings'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.PATH_SETTINGS_BUTTON).click()

    def assignLearnersCohortsManually(self, email):
        '''Asign learners cohort manually'''
        self.openManageStudents()
        self.logger.do_click('Email address = ' + email)
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_PASSWORD).send_keys(email)
        self.logger.do_click('Add Students')
        self.driver.find_element_by_xpath(self.PATH_ADD_STUDENTS_BUTTON).click()
        time.sleep(3)

    def add_content_group(self, groupName):
        '''Add content group'''
        self.openSettings()
        self.logger.do_click('Select content group')
        self.driver.find_element_by_xpath(self.PATH_SELECT_CONTENT_GROUP_BUTTON).click()
        self.logger.do_click('Content group name = ' + groupName)
        self.driver.find_element_by_xpath(self.PATH_CONTENT_GROUP_NAME_FIELD).send_keys(groupName)
        self.logger.do_click('Save')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(1)



    def get_cohorts_status(self):
        '''Get cohorts status'''
        return self.driver.find_element_by_xpath(self.PATH_ENABLE_COHORTS_BUTTON).get_attribute("checked")

    def get_possible_add_cohorts(self):
        '''Get possible add cohorts'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_ADD_COHORTS_BUTTON).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_cohorts_compound(self):
        '''Get cohorts сompound'''
        return self.driver.find_element_by_xpath(self.PATH_COHORTS_FIELD).text.replace(' ', '').replace('\n\n', ';')

    def get_prompt_cohort_contains_student(self):
        '''Get prompt cohort contains student'''
        return self.driver.find_element_by_xpath(self.PATH_PROMPT_COHORT_CONTAINS_STUDENT).text

    def get_prompt_saved_cohort(self):
        '''Get prompt saved cohort'''
        return self.driver.find_element_by_xpath(self.PATH_PROMPT_SAVED_COHORT).text