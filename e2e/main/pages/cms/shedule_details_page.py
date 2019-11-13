import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class SheduleDetailsPage():

    PATH_SCHEDULE_DETAILS_BUTTON = "//a[contains(text(), 'Schedule & Details')]"

    PATH_COURSE_START_FIELD = "//input[@id='course-start-date']"
    PATH_COURSE_END_FIELD = "//input[@id='course-end-date']"
    PATH_ENROLLMENT_START_FIELD = "//input[@id='course-enrollment-start-date']"
    PATH_ENROLLMENT_END_FIELD = "//input[@id='course-enrollment-end-date']"
    PATH_SELF_PACED_BUTTON = "//input[@id='course-pace-self-paced']"

    PATH_COURSE_LENGUAGE_FIELD = "//select[@id='course-language']"
    PATH_COURSE_SHORT_DESCRIPTION_FIELD = "//textarea[@id='course-short-description']"
    PATH_COURSE_HOURS_EFFORT_FIELD = "//input[@id='course-effort']"
    PATH_PREREQUISITE_COURSE_FIELD = "//select[@id='pre-requisite-course']"

    PATH_ENTRANCE_EXAM_BUTTON = "//input[@id='entrance-exam-enabled']"

    PATH_ALL_RIGHT_RESERVED_BUTTON = "//button[@name='license-all-rights-reserved']"
    PATH_CREATIVE_COMMON_BUTTON = "//button[@name='license-creative-commons']"

    PATH_ATTRIBUTION_BUTTON = "//ul[@class='license-options']/li[1]/input"
    PATH_NONCOMMERCIAL_BUTTON = "//ul[@class='license-options']/li[2]/input"
    PATH_NO_DERIVATIVES_BUTTON = "//ul[@class='license-options']/li[3]/input"
    PATH_SHARE_ALIKE_BUTTON = "//ul[@class='license-options']/li[4]/input"

    PATH_SAVE_CHANGES_BUTTON = "//button[contains(text(), 'Save Changes')]"

    def __init__(self, driver, *args, **kwargs):
        super(SheduleDetailsPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)

    def open_shedule_details(self):
        '''Open Shedule & details'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_SETTINGS_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Shedule & details')
        self.driver.find_element_by_xpath(self.PATH_SCHEDULE_DETAILS_BUTTON).click()
        time.sleep(3)

    def set_course_self_paced(self):
        '''Set course self paced'''
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SELF_PACED_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Self Paced')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def input_date(self, courseStart, courseEnd, enrollmentStart, enrollmentEnd):
        '''Input date'''
        self.logger.do_input('Course Start Date = "' + courseStart + '"')
        self.config.scroll_to_element("xpath", "//h2[contains(text(), 'Course Details')]")
        time.sleep(1)
        self.driver.find_element_by_xpath(self.PATH_COURSE_START_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_COURSE_START_FIELD).send_keys(courseStart)
        self.driver.find_element_by_xpath(self.PATH_COURSE_START_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.logger.do_input('Course End Date = "' + courseEnd + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_END_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_COURSE_END_FIELD).send_keys(courseEnd)
        self.driver.find_element_by_xpath(self.PATH_COURSE_END_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.logger.do_input('Enrollment Start Date = "' + enrollmentStart + '"')
        self.driver.find_element_by_xpath(self.PATH_ENROLLMENT_START_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ENROLLMENT_START_FIELD).send_keys(enrollmentStart)
        self.driver.find_element_by_xpath(self.PATH_ENROLLMENT_START_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.logger.do_input('Enrollment End Date = "' + enrollmentEnd + '"')
        self.driver.find_element_by_xpath(self.PATH_ENROLLMENT_END_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ENROLLMENT_END_FIELD).send_keys(enrollmentEnd)
        self.driver.find_element_by_xpath(self.PATH_ENROLLMENT_END_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def input_course_lenguage(self, value):
        '''Input Course lenguage'''
        self.logger.do_input('Course Lenguage = "' + value + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_LENGUAGE_FIELD).send_keys(value)
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def input_course_short_description(self, value):
        '''Input Course Short Description'''
        self.logger.do_input('Course Short Description = "' + value + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_SHORT_DESCRIPTION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_COURSE_SHORT_DESCRIPTION_FIELD).send_keys(value)
        self.driver.find_element_by_xpath(self.PATH_COURSE_SHORT_DESCRIPTION_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def input_course_overview(self, filePath):
        '''Input Course Overview'''
        self.logger.do_input('Course Overview')
        search_bar = self.driver.find_element_by_xpath("//div[@class='CodeMirror-code']/div[2]/pre/span")
        actions = ActionChains(self.driver)
        actions.click(search_bar)
        actions.click()
        actions.send_keys(Keys.ARROW_LEFT)
        for i in range(1, 2000):
            actions.send_keys(Keys.DELETE)
        for i in range(1, 500):
            actions.send_keys(Keys.BACK_SPACE)
        actions.perform()

        file = open(variables.PATH_TO_LIB + filePath, 'r')
        fileList = file.read()
        self.config.execute_script_input("//div[@class='CodeMirror-code']/div[1]", fileList)
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def input_course_hours_effort(self, value):
        '''Input Course Overview'''
        self.logger.do_input('Hours of Effort = "' + value + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_HOURS_EFFORT_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_COURSE_HOURS_EFFORT_FIELD).send_keys(value)
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def set_prerequisite_course(self, course):
        '''Set Prerequisite Course'''
        self.logger.do_input('Prerequisite Course = "' + course + '"')
        self.driver.find_element_by_xpath(self.PATH_PREREQUISITE_COURSE_FIELD).send_keys(course)
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def set_entrance_exam(self):
        '''Set entrance exam'''
        self.logger.do_click('Entrance Exam')
        self.driver.find_element_by_xpath(self.PATH_ENTRANCE_EXAM_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def set_course_license_all(self):
        '''Input Course Overview'''
        self.logger.do_click('All Rights Reserved')
        self.driver.find_element_by_xpath(self.PATH_ALL_RIGHT_RESERVED_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
        time.sleep(3)

    def set_course_license(self, line, activity):
        '''Input licence noncommercial'''
        number = "0"
        if(line == variables.TEXT_ATTRIBUTION):
            number = "1"
        elif(line == variables.TEXT_NONCOMMERCIAL):
            number = "2"
        elif(line == variables.TEXT_NO_DERIVATIVES):
            number = "3"
        elif(line == variables.TEXT_SHARE_ALIKE):
            number = "4"
        else:
            print("Incorrect line")
            self.config.do_assert_true(1, 2)

        self.logger.do_click('Creative Commons')
        self.config.scroll_to_element("xpath", "//div[@class='colophon']")
        self.driver.find_element_by_xpath(self.PATH_CREATIVE_COMMON_BUTTON).click()
        time.sleep(1)
        if (activity == variables.STATUS_ON):
            if (self.driver.find_element_by_xpath("//ul[@class='license-options']/li[" + number + "]/input").is_selected()):
                pass
            else:
                self.logger.do_click('Noncommercial')
                self.driver.find_element_by_xpath("//ul[@class='license-options']/li[" + number + "]/input").click()
                time.sleep(1)
        else:
            if (self.driver.find_element_by_xpath("//ul[@class='license-options']/li[" + number + "]/input").is_selected()):
                self.logger.do_click('Noncommercial')
                self.driver.find_element_by_xpath("//ul[@class='license-options']/li[" + number + "]/input").click()
                time.sleep(1)
            else:
                pass
        try:
            self.logger.do_click('Save changes')
            self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
            time.sleep(3)
        except:
            pass
