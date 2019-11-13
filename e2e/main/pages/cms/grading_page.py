import time
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class GradingPage():

    PATH_GRADING_BUTTON = "//a[contains(text(), 'Grading')]"
    PATH_DELETE_TYPE_BUTTON = "//a[@class='button delete-button standard remove-item remove-grading-data']"
    PATH_NEW_TYPE_BUTTON = "//a[@class='new-button new-course-grading-item add-grading-data']"
    PATH_SAVE_CHANGES_BUTTON = "//button[contains(text(), 'Save Changes')]"

    PATH_TYPE_NAME_FIELD = "//input[@id='course-grading-assignment-name']"
    PATH_ABBREAVIATION_FIELD = "//input[@id='course-grading-assignment-shortname']"
    PATH_WEIGHT_FIELD = "//input[@id='course-grading-assignment-gradeweight']"
    PATH_TOTAL_NUMBER_FIELD = "//input[@id='course-grading-assignment-totalassignments']"
    PATH_NUMBER_DROPPABLE_FIELD = "//input[@id='course-grading-assignment-droppable']"

    def __init__(self, driver, *args, **kwargs):
        super(GradingPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.course_outline_page = CourseOutlinePage(self.driver)

    def open_grading(self):
        '''Open Grading'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_SETTINGS_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Grading')
        self.driver.find_element_by_xpath(self.PATH_GRADING_BUTTON).click()
        time.sleep(3)

    def delete_all_types(self):
        '''Delete aa types'''
        try:
            for i in range(1, 10):
                self.logger.do_click('Delete')
                self.driver.find_element_by_xpath(self.PATH_DELETE_TYPE_BUTTON).click()
                time.sleep(1)
                self.logger.do_click('Save')
                self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
                time.sleep(3)
        except NoSuchElementException:
            pass

    def create_type(self, longName, shortName, weight, totalNumber, droppableNumber):
        '''Create type'''
        self.logger.do_click('New type')
        self.driver.find_element_by_xpath(self.PATH_NEW_TYPE_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('Type name = "' + longName + '"')
        self.driver.find_element_by_xpath(self.PATH_TYPE_NAME_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_TYPE_NAME_FIELD).send_keys(longName)
        self.logger.do_input('Abbreaviation = "' + shortName + '"')
        self.driver.find_element_by_xpath(self.PATH_ABBREAVIATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ABBREAVIATION_FIELD).send_keys(shortName)
        self.logger.do_input('Weight = "' + weight + '"')
        self.driver.find_element_by_xpath(self.PATH_WEIGHT_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_WEIGHT_FIELD).send_keys(weight)
        self.logger.do_input('Total number = "' + totalNumber + '"')
        self.driver.find_element_by_xpath(self.PATH_TOTAL_NUMBER_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_TOTAL_NUMBER_FIELD).send_keys(totalNumber)
        self.logger.do_input('Number droppable = "' + droppableNumber + '"')
        self.driver.find_element_by_xpath(self.PATH_NUMBER_DROPPABLE_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_NUMBER_DROPPABLE_FIELD).send_keys(droppableNumber)
        time.sleep(1)
        self.logger.do_click('Save')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)