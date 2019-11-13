import time
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger

class ProgressPage():
    PATH_PROGRESS_BUTTON = "//a[contains(@href, 'progress')]"
    PATH_REQUEST_CERTIFICATE = "//button[contains(text(), 'Request Certificate')]"
    PATH_VIEW_CERTIFICATE = "//a[contains(text(), 'View Certificate ')]"
    PATH_CERTIFICATES = "//div[@class='wrapper-view']"
    PATH_SUBSECTIONS_RESULT = "//div[@class='sections']"
    PATH_GRADE_RESULT = "//div[@class='grade-detail-graph']"


    def __init__(self, driver, *args, **kwargs):
        super(ProgressPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)

    def open_progress(self):
        '''Open Progress'''
        self.logger.do_click('Progress')
        self.driver.find_element_by_xpath(self.PATH_PROGRESS_BUTTON).click()
        time.sleep(8)

    def click_request_certificate(self):
        '''Click Request Certificate'''
        self.logger.do_click('Request Certificate')
        self.driver.find_element_by_xpath(self.PATH_REQUEST_CERTIFICATE).click()
        time.sleep(3)

    def click_view_certificate(self):
        '''Click View Certificate '''
        self.logger.do_click('View Certificate')
        self.driver.find_element_by_xpath(self.PATH_VIEW_CERTIFICATE).click()
        time.sleep(3)



    def get_certificate_text(self):
        '''Get certificates text'''
        return self.driver.find_element_by_xpath(self.PATH_CERTIFICATES).text

    def get_subsection_result_text(self):
        '''Get subsection result'''
        return self.driver.find_element_by_xpath(self.PATH_SUBSECTIONS_RESULT).text.replace('\n', '; ')

    def get_grade_result_text(self):
        '''Get grade result'''
        return self.driver.find_element_by_xpath(self.PATH_GRADE_RESULT).text.replace('\n', '; ')

    def get_present_progress_graph(self):
        '''Get present progress graph'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_GRADE_RESULT).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_present_request_certificate(self):
        '''Get present request certificate'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_REQUEST_CERTIFICATE).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

