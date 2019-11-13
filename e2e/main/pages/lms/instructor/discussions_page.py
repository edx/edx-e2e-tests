import time
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables

class DiscussionsPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_DISCUSSIONS_BUTTON = "//button[contains(text(), 'Discussions')]"
    PATH_NOT_DIVIDENT_BUTTON = "//input[@class='division-scheme none']"
    PATH_COHORTS_BUTTON = "//input[@class='division-scheme cohort']"
    PATH_GENERAL_BUTTON = "//input[@class='check-discussion-subcategory-course-wide']"
    PATH_SAVE_BUTTON = "//button[contains(text(), 'Save')]"

    def __init__(self, driver, *args, **kwargs):
        super(DiscussionsPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()

    def open_discussions(self):
        '''Open discussions'''
        self.logger.do_click('Instructor')
        self.driver.find_element_by_xpath(self.PATH_INSTRUCTOR_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Discussions')
        self.driver.find_element_by_xpath(self.PATH_DISCUSSIONS_BUTTON).click()
        time.sleep(5)

    def set_cohorts_on(self):
        '''Set instructor on'''
        self.logger.do_click('Cohorts')
        self.driver.find_element_by_xpath(self.PATH_COHORTS_BUTTON).click()
        time.sleep(1)
        if(self.driver.find_element_by_xpath(self.PATH_GENERAL_BUTTON).is_selected()):
            self.logger.do_click('General')
            self.driver.find_element_by_xpath(self.PATH_GENERAL_BUTTON).click()
            time.sleep(1)
            self.logger.do_click('General')
            self.driver.find_element_by_xpath(self.PATH_GENERAL_BUTTON).click()
            time.sleep(1)
        else:
            self.logger.do_click('General')
            self.driver.find_element_by_xpath(self.PATH_GENERAL_BUTTON).click()
            time.sleep(1)
        self.logger.do_click('Save')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(3)

    def set_cohorts_off(self):
        '''Set instructor on'''
        self.logger.do_click('Cohorts')
        self.driver.find_element_by_xpath(self.PATH_NOT_DIVIDENT_BUTTON).click()
        time.sleep(1)