import time

from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables

class CourseInfoPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_COURSE_INFO_BUTTON = "//button[contains(text(), 'Course Info')]"
    PATH_CLICKING_HERE_BUTTON = "//a[contains(text(), 'by clicking here')]"
    PATH_INFO_ENROLLMENT = "//div[@class='enrollment-wrapper']"
    PATH_COURSE_INFO = "//div[@class='basic-wrapper']"

    def __init__(self, driver, *args, **kwargs):
        super(CourseInfoPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_course_info(self):
        '''Open cohorts info'''
        self.logger.do_click('Instructor')
        self.config.scroll_to_element("xpath", self.PATH_INSTRUCTOR_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_INSTRUCTOR_BUTTON).click()
        time.sleep(3)
        self.config.switch_window(0)
        self.logger.do_click('Course info')
        self.driver.find_element_by_xpath(self.PATH_COURSE_INFO_BUTTON).click()
        time.sleep(3)

    def click_by_clicking_here(self):
        '''Click by clicking here'''
        self.logger.do_click('by clicking here')
        self.driver.find_element_by_xpath(self.PATH_CLICKING_HERE_BUTTON).click()
        time.sleep(3)


    def get_info_enrollment_table_information(self):
        '''Get info enrollment information'''
        return self.driver.find_element_by_xpath(self.PATH_INFO_ENROLLMENT).text.replace('\n', '; ')

    def get_info_course_information(self):
        '''Get info course information'''
        return self.driver.find_element_by_xpath(self.PATH_COURSE_INFO).text.replace('\n', '; ')