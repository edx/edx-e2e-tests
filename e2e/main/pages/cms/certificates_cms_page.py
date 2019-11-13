import time
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class CertificatesCmsPage():

    PATH_CERTIFICATE_DETAILS = "//h2[contains(text(), 'Certificate Details')]"
    PATH_CERTIFICATES_BUTTON = "//a[contains(text(), 'Certificates')]"
    PATH_SETUP_CERTIFICATES_BUTTON = "//a[@class='button new-button']"
    PATH_CREATE_BUTTON = "//button[contains(text(), 'Create')]"
    PATH_ACTIVATE_BUTTON = "//button[@class='button activate-cert']"
    PATH_PREVIEW_BUTTON = "//div[@class='preview-certificate nav-actions']/a"
    PATH_CERTIFICATES = "//div[@class='certificate-body'] | //div[@class='wrapper-view']"

    def __init__(self, driver, *args, **kwargs):
        super(CertificatesCmsPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.course_outline_page = CourseOutlinePage(self.driver)



    def open_certificates(self):
        '''Open certificate'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_SETTINGS_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Group Configuration')
        self.driver.find_element_by_xpath(self.PATH_CERTIFICATES_BUTTON).click()
        time.sleep(3)

    def setup_certificate(self):
        '''set up certificate'''
        self.logger.do_click('Set up your certificate')
        self.driver.find_element_by_xpath(self.PATH_SETUP_CERTIFICATES_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Create')
        self.driver.find_element_by_xpath(self.PATH_CREATE_BUTTON).click()
        time.sleep(3)

    def activate_certificate(self):
        '''Activate certificate'''
        self.logger.do_click('Activate')
        self.driver.find_element_by_xpath(self.PATH_ACTIVATE_BUTTON).click()
        time.sleep(3)

    def click_preview(self):
        '''Click preview'''
        self.logger.do_click('Preview')
        self.driver.find_element_by_xpath(self.PATH_PREVIEW_BUTTON).click()
        time.sleep(3)



    def get_certificate_details_text(self):
        '''Get Certificate details'''
        return self.driver.find_element_by_xpath(self.PATH_CERTIFICATE_DETAILS).text

    def get_certificate_includes_text(self):
        '''Get Certificate present text'''
        return self.driver.find_element_by_xpath(self.PATH_CERTIFICATES).text