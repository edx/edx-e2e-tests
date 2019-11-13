import time
from e2e.main.conf import variables
from e2e.main.conf.logger import Logger

class CertificatesLmsPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_CERTIFICATES_BUTTON = "//button[contains(text(), 'Certificates')]"
    PATH_ENABLE_CERTIFICATES_BUTTON = "//input[@id='enable-certificates-submit']"
    PATH_DISABLE_CERTIFICATES_BUTTON = "//input[@id='disable-certificates-submit']"

    def __init__(self, driver, *args, **kwargs):
        super(CertificatesLmsPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()



    def open_certificates(self):
        '''Open membership'''
        self.logger.do_click('Certificates')
        self.driver.find_element_by_xpath(self.PATH_CERTIFICATES_BUTTON).click()
        time.sleep(1)

    def set_certificates(self, status):
        '''Open membership'''
        if(status == variables.STATUS_ON):
            self.logger.do_click('Enable')
            self.driver.find_element_by_xpath(self.PATH_ENABLE_CERTIFICATES_BUTTON).click()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
            time.sleep(3)
        elif(status == variables.STATUS_OFF):
            self.logger.do_click('Disable')
            self.driver.find_element_by_xpath(self.PATH_DISABLE_CERTIFICATES_BUTTON).click()

