import time
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables

class OpenResponsesPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_OPEN_RESPONSES_BUTTON = "//button[contains(text(), 'Open Responses')]"
    PATH_OPEN_RESPONSE_ASSESSMENT_BUTTON = "//a[contains(text(), 'Open Response Assessment')]"
    PATH_BACK_TO_FULL_LIST_BUTTON = "//a[contains(text(), 'Back to Full List')]"

    PATH_OPEN_RESPONSE_TEXT = "//section[@class='open-response-assessment']"

    def __init__(self, driver, *args, **kwargs):
        super(OpenResponsesPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_open_responses(self):
        '''Open open responses'''
        self.logger.do_click('Instructor')
        self.config.execute_script_click(self.PATH_INSTRUCTOR_BUTTON)
        time.sleep(1)
        self.config.switch_window(0)
        self.logger.do_click('Open Responses')
        self.driver.find_element_by_xpath(self.PATH_OPEN_RESPONSES_BUTTON).click()
        time.sleep(3)

    def open_some_response_assessment(self):
        '''Open some response assessment'''
        self.logger.do_click('Open Response Asseesment')
        self.driver.find_element_by_xpath(self.PATH_OPEN_RESPONSE_ASSESSMENT_BUTTON).click()
        time.sleep(3)

    def click_back_to_full_list(self):
        '''Click back to full list'''
        self.logger.do_click('Back to full list')
        self.driver.find_element_by_xpath(self.PATH_BACK_TO_FULL_LIST_BUTTON).click()
        time.sleep(3)


    def get_open_responses_text(self):
        '''Get open responses text'''
        return self.driver.find_element_by_xpath(self.PATH_OPEN_RESPONSE_TEXT).text.replace('\n', '; ')