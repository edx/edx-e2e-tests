import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger

class CoursesPage():
    PATH_COURSES_BUTTON = "//a[contains(text(), 'Find courses')] | //a[contains(text(), 'Explore courses')] | //input[@id='discovery-input'] | //a[contains(text(), 'Discover New')]"
    PATH_LOGO_BUTTON = "//img[@class='logo'] | //img[@class='logo-en']"
    PATH_COURSES_TEXT = "//div[@class='courses'] | //div[@class='courses no-course-discovery'] | //div[@class='my-courses']"
    PATH_ENROLL_BUTTONT = "//a[@class='register']"
    PATH_VIEW_BUTTONT = "//strong[contains(text(), 'View Course')]"
    PATH_INVITATION_ONLY_BUTTONT = "//span[@class='register disabled']"
    PATH_TEXT_ABOUT_PAGE = "//section[@class='course-info']"

    PATH_CLEAR_ALL_BUTTONT = "//button[@id='clear-all-filters']"
    PATH_REFINE_YOUR_SEARCH = "//section[@class='search-facets-lists']"


    def __init__(self, driver, *args, **kwargs):
        super(CoursesPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_courses(self):
        '''Open Courses'''
        if(variables.PROJECT in variables.PROJECT_E4H):
            self.config.input_url(variables.URL_COURSES)
        else:
            self.logger.do_click('Courses')
            self.config.wait_element(self.PATH_COURSES_BUTTON)
            self.driver.find_element_by_xpath(self.PATH_COURSES_BUTTON).click()
            time.sleep(3)

    def scroll_oll_page(self):
        '''Open Courses'''
        self.logger.do_click('Page Down')
        for i in range(1, 1500):
            self.driver.find_element_by_xpath(self.PATH_COURSES_BUTTON).send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        self.logger.do_click('Page Up')
        for i in range(1, 500):
            self.driver.find_element_by_xpath(self.PATH_COURSES_BUTTON).send_keys(Keys.PAGE_UP)
        time.sleep(1)

    def open_dashboard(self):
        '''Open Dashboard'''
        if (variables.PROJECT in variables.PROJECT_E4H):
            self.config.input_url(variables.URL_DASHBOARD)
        else:
            self.logger.do_click('Dashboard')
            self.driver.find_element_by_xpath(self.PATH_LOGO_BUTTON).click()
            time.sleep(3)

    def search_by_text(self, value):
        '''Search by some text'''
        self.logger.do_input('Search by "' + value + '"')
        self.driver.find_element_by_xpath("//input[@id='discovery-input']").clear()
        self.driver.find_element_by_xpath("//input[@id='discovery-input']").send_keys(value)
        time.sleep(1)
        self.logger.do_click('Search')
        self.driver.find_element_by_xpath("//span[@class='icon fa fa-search']").click()
        time.sleep(3)

    def search_by_refine(self, value):
        '''Search by some refine'''
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//button[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def reset_search(self, value):
        '''Reset search'''
        if(value is variables.EMPTY):
            self.logger.do_click('Clear All')
            self.driver.find_element_by_xpath(self.PATH_CLEAR_ALL_BUTTONT).click()
        else:
            self.logger.do_click(value)
            self.driver.find_element_by_xpath("//span[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def open_created_course(self, courseid):
        '''Open Course'''
        self.logger.do_click('Created course')
        self.driver.find_element_by_xpath("//a[@href='/courses/" + courseid + "/about']").click()
        time.sleep(3)

    def click_enroll(self):
        '''Click Enroll'''
        self.logger.do_click('Enroll')
        self.driver.find_element_by_xpath(self.PATH_ENROLL_BUTTONT).click()
        time.sleep(3)

    def click_view(self):
        '''Click VIEW COURSE'''
        self.logger.do_click('Enroll')
        self.driver.find_element_by_xpath(self.PATH_VIEW_BUTTONT).click()
        time.sleep(3)

    def click_invitation_only(self):
        '''Click Invitation only'''
        self.logger.do_click('Invitation only')
        self.driver.find_element_by_xpath(self.PATH_INVITATION_ONLY_BUTTONT).click()
        time.sleep(3)

    def open_prerequisites_course(self, name):
        '''Open prerequisites course'''
        self.logger.do_click('Prerequisites Course')
        self.driver.find_element_by_xpath("//a[contains(text(), '" + name + "')]").click()
        time.sleep(3)



    def get_courses_list_text(self):
        '''Get text about courses'''
        return self.driver.find_element_by_xpath(self.PATH_COURSES_TEXT).text.replace('\n', '; ')

    def get_possible_enroll(self):
        '''Get possible enroll'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_ENROLL_BUTTONT).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_text_about_page(self):
        '''Get text about courses'''
        return self.driver.find_element_by_xpath(self.PATH_TEXT_ABOUT_PAGE).text.replace('\n', '; ').lower()

    def get_text_refine_your_search(self):
        '''Get text about courses'''
        return self.driver.find_element_by_xpath(self.PATH_REFINE_YOUR_SEARCH).text.replace('\n', '; ')