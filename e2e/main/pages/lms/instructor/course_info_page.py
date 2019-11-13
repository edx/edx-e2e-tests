import time
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables

class CourseInfoPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_COHORTS_BUTTON = "//button[contains(text(), 'Course Info')]"
    PATH_INFO_ENROLLMENT_FIELD = "//div[@class='enrollment-wrapper']"

    def __init__(self, driver, *args, **kwargs):
        super(CourseInfoPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()



    def open_course_info(self):
        '''Open cohorts info'''
        self.logger.do_click('Instructor')
        self.driver.find_element_by_xpath(self.PATH_INSTRUCTOR_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Course info')
        self.driver.find_element_by_xpath(self.PATH_COHORTS_BUTTON).click()
        time.sleep(1)



    def get_info_enrollment_table_information(self):
        '''Get info enrollment information'''
        return self.driver.find_element_by_xpath(self.PATH_INFO_ENROLLMENT_FIELD).text.replace('\n', '; ')