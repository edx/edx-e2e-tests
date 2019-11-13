import time
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class CourseUpdatesPage():

    PATH_UPDATES_BUTTON = "//a[contains(text(), 'Updates')]"
    PATH_NEW_UPDATE_BUTTON = "//a[@class=' button new-button new-update-button']"
    PATH_EDIT_UPDATE_BUTTON = "//button[@class='edit-button']"
    PATH_DELETE_UPDATE_BUTTON = "//button[@class='delete-button']"
    PATH_EDIT_HANGOUTS_BUTTON = "//div[@class='sidebar course-handouts']/a"
    PATH_POST_BUTTON = "//button[contains(text(), 'Post')]"
    PATH_SAVE_BUTTON = "//a[contains(text(), 'Save')]"
    PATH_COURSE_UPDATE_FIELD = "//div[@class='CodeMirror-code']/div[1]"
    PATH_COURSE_HANDOUT_FIELD = "//div[@class='CodeMirror-code']"
    PATH_ABOUT_COURSE = "//div[@class='course-info-wrapper']"
    PATH_OK_BUTTON = "//button[contains(text(), 'OK')]"

    def __init__(self, driver, *args, **kwargs):
        super(CourseUpdatesPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)

    def open_course_updates(self):
        '''Open Course updates'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_CONTENT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Updates')
        self.driver.find_element_by_xpath(self.PATH_UPDATES_BUTTON).click()
        time.sleep(5)

    def input_course_update(self, text):
        '''Input course update'''
        self.logger.do_click('New Update')
        self.driver.find_element_by_xpath(self.PATH_NEW_UPDATE_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('Value = "' + text + '"')
        self.config.execute_script_input(self.PATH_COURSE_UPDATE_FIELD, text)
        time.sleep(1)
        self.logger.do_click('Post')
        self.driver.find_element_by_xpath(self.PATH_POST_BUTTON).click()
        time.sleep(3)

    def edit_course_update(self, text):
        '''Edit course update'''
        self.logger.do_click('New Update')
        self.driver.find_element_by_xpath(self.PATH_EDIT_UPDATE_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('Value = "' + text + '"')
        self.config.execute_script_input(self.PATH_COURSE_UPDATE_FIELD, text)
        self.logger.do_click('Post')
        self.driver.find_element_by_xpath(self.PATH_POST_BUTTON).click()
        time.sleep(3)

    def delete_course_update(self):
        '''Delete course update'''
        self.logger.do_click('Delete')
        self.driver.find_element_by_xpath(self.PATH_DELETE_UPDATE_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('OK')
        self.driver.find_element_by_xpath(self.PATH_OK_BUTTON).click()
        time.sleep(3)

    def input_course_handouts(self, text):
        '''Input course hangouts'''
        self.logger.do_click('Edit')
        self.driver.find_element_by_xpath(self.PATH_EDIT_HANGOUTS_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('Value = "' + text + '"')
        self.config.execute_script_input(self.PATH_COURSE_HANDOUT_FIELD, "<p>" + text)
        time.sleep(1)
        self.logger.do_click('Save changes')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(3)



    def get_about_course_text(self):
        '''Get course updates and course handouts'''
        return self.driver.find_element_by_xpath(self.PATH_ABOUT_COURSE).text.replace('\n', '; ')
