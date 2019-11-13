import time
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.conf.config import Config

class AdvancedSettingsPage():

    PATH_ADVANCED_SETTINGS_BUTTON = "//a[contains(text(), 'Advanced Settings')]"
    PATH_DAYS_EARLI_FOR_BETA_USERS = "//div[@id='days_early_for_beta']/following-sibling::div/div/div[6]/div/div/div/div/div[3]/pre/span"
    PATH_SAVE_CHANGES_BUTTON = "//button[contains(text(), 'Save Changes')]"


    def __init__(self, driver, *args, **kwargs):
        super(AdvancedSettingsPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)



    def open_advanced_settings(self):
        '''Open Advanced Settings'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_SETTINGS_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Advanced Settings')
        self.driver.find_element_by_xpath(self.PATH_ADVANCED_SETTINGS_BUTTON).click()
        time.sleep(3)

    def set_value_advanced_setting(self, element, value):
        '''Set value advanced setting'''
        line = "//div[@id='" + element + "']/following-sibling::div/div/div[6]/div/div/div/div/div[3]/pre/span"
        if(value not in (self.driver.find_element_by_xpath(line).text)):
            self.logger.do_input('Set value for "' + element + '" = "' + value + '"')
            self.config.execute_script_input(line, value)
            self.driver.find_element_by_xpath(self.PATH_SAVE_CHANGES_BUTTON).click()
            time.sleep(3)






