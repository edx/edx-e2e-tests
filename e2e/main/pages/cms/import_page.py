import time
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class ImportPage():

    PATH_IMPORT_BUTTON = "//a[contains(text(), 'Import')]"
    PATH_FILE_FIELD = '//input[@type="file"]'
    PATH_REPLASE_BUTTON = '//input[@id="replace-courselike-button"]'
    PATH_VIEW_UPDATED_OUTLINE_BUTTON = '//a[@id="view-updated-button"]'

    def __init__(self, driver, *args, **kwargs):
        super(ImportPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)

    def open_import(self):
        '''Open import'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_TOOLS_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Import')
        self.driver.find_element_by_xpath(self.PATH_IMPORT_BUTTON).click()
        time.sleep(3)

    def import_course(self, fileName):
        '''Upload a tarball to be imported.'''
        asset_file_path = variables.PATH_TO_LIB + fileName
        self.driver.execute_script('$(".file-name-block").show();$(".file-input").show()')
        self.logger.do_input('Path to file = "' + variables.PATH_TO_LIB + fileName + '"')
        self.driver.find_element_by_xpath(self.PATH_FILE_FIELD).send_keys(asset_file_path)
        self.driver.find_element_by_xpath(self.PATH_FILE_FIELD).send_keys(asset_file_path)
        self.logger.do_click('Replase')
        self.driver.find_element_by_xpath(self.PATH_REPLASE_BUTTON).click()
        self.logger.do_click('View Updated Outline')
        self.config.wait_element(self.PATH_VIEW_UPDATED_OUTLINE_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_VIEW_UPDATED_OUTLINE_BUTTON).click()
        time.sleep(3)
        self.driver.implicitly_wait(10)
