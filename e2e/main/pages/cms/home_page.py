import time
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class HomePage():
    PATH_HOME_PAGE = "//a[@class='brand-link']"
    PATH_LIST_COURSES = "//ul[@class='list-courses'] | //ul[@class='list-courses courses-list'] | //article[@class='content-primary']"

    def __init__(self, driver, *args, **kwargs):
        super(HomePage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)

    def open_home(self):
        '''Open Outline'''
        self.logger.do_click('Home')
        self.driver.find_element_by_xpath(self.PATH_HOME_PAGE).click()
        time.sleep(3)



    def get_courses_list_text(self):
        '''Get list courses'''
        return self.driver.find_element_by_xpath(self.PATH_LIST_COURSES).text.replace('\n', '; ')