import time
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables
from e2e.main.conf.config import Config

class DashboardPage():

    PATH_DASHBOARD_BUTTON = "//img[@class='logo'] | //img[@class='logo-en']"
    PATH_LOGIN_WAIT = "//span[@class='username'] | //div[@class='label-username'] | //h1[@class='page-header'] | //a[contains(text(), 'View site')] | //a[contains(text(), 'Certificate generation configurations')]"
    PATH_USERNAME_FIELD = "//span[@class='username'] | //div[@class='label-username']"
    PATH_MY_COURSE = "//header[@class='wrapper-header-courses']/h2"
    PATH_SYSADMIN_BUTTON = "//a[@href='/sysadmin/']"
    PATH_TEST_COURSE = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/info'] | //a[@href='/courses/" + variables.ID_BASE_COURSE + "/course/']"
    PATH_TEST_COURSE_TEXT = "//section[@aria-labelledby='details-heading-" + variables.ID_BASE_COURSE + "']"
    PATH_TEXT_DASHBOARD_COURSES = "//ul[@class='listing-courses'] | //div[@class='empty-dashboard-message']"
    PATH_VIEW_COURSE_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/info'] | //a[@href='/courses/" + variables.ID_BASE_COURSE + "/course/']"

    PATH_DROP_DOWN_BUTTON = "//div[@class='toggle-user-dropdown'] | //button[@class='dropdown'] | " \
                            "//li[@class='nav-item nav-account-user']/h3/span[2] | //button[@class='user-dropdown']/span[2] | " \
                            "//button[@class='menu-button button-more has-dropdown js-dropdown-button']/span"
    PATH_ENROLLED_COURSES_BUTTON = "//a[contains(text(), 'Enrolled Courses')]"
    PATH_SIGN_OUT_BUTTON = "//a[contains(text(), 'Sign Out')]"

    def __init__(self, driver, *args, **kwargs):
        super(DashboardPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_dashboard(self):
        '''Logout user'''
        if(variables.PROJECT in variables.PROJECT_LETSTUDY + variables.PROJECT_ASUOSPP):
            self.config.input_url(variables.URL_DASHBOARD)
        else:
            self.logger.do_click('Logo')
            self.driver.find_element_by_xpath(self.PATH_DASHBOARD_BUTTON).click()
        time.sleep(3)


    def open_enrolled_courses(self):
        '''Logout user'''
        self.logger.do_click('Drop down')
        self.driver.find_element_by_xpath(self.PATH_DROP_DOWN_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Enrolled courses')
        self.driver.find_element_by_xpath(self.PATH_ENROLLED_COURSES_BUTTON).click()
        time.sleep(1)

    def open_cours(self):
        '''Open course Base'''
        self.logger.do_click('Test course "' + variables.ID_BASE_COURSE + '"')
        self.driver.find_element_by_xpath(self.PATH_TEST_COURSE).click()
        time.sleep(1)

    def open_created_cours(self, organization, courseNumber, courseRun):
        '''Open course'''
        self.logger.do_click('Test course "' + organization + "+" + courseNumber + "+" + courseRun + '"')
        self.config.wait_element("//a[@href='/courses/" + variables.ID + organization + "+" + courseNumber + "+" + courseRun + "/info'] | "
                                          "//a[@href='/courses/" + variables.ID + organization + "+" + courseNumber + "+" + courseRun + "/course/']")
        self.driver.find_element_by_xpath("//a[@href='/courses/" + variables.ID + organization + "+" + courseNumber + "+" + courseRun + "/info'] | "
                                          "//a[@href='/courses/" + variables.ID + organization + "+" + courseNumber + "+" + courseRun + "/course/']").click()
        time.sleep(3)

    def open_prerequisites_course(self, name):
        '''Open course'''
        self.logger.do_click('Open Prerequisites Course')
        self.driver.find_element_by_xpath("//a[contains(text(), '" + name + "')]").click()
        time.sleep(1)

    def logout(self):
        '''Logout user'''
        self.logger.do_click('Drop down')
        self.driver.find_element_by_xpath(self.PATH_DROP_DOWN_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Logout')
        self.driver.find_element_by_xpath(self.PATH_SIGN_OUT_BUTTON).click()
        time.sleep(3)



    def get_my_course_text(self):
        '''Get text 'My Course' on dashboard page'''
        return self.driver.find_element_by_xpath(self.PATH_MY_COURSE).text.lower()

    def get_dashboard_courses_list_text(self):
        '''Get text dashboard courses'''
        return self.driver.find_element_by_xpath(self.PATH_TEXT_DASHBOARD_COURSES).text.lower().replace('\n', '; ')

    def get_present_button_view_course(self, courseid):
        '''Get present button View course'''
        result = "1"
        try:
            self.driver.find_element_by_xpath("//a[@href='/courses/" + courseid + "/info'] | "
                                              "//a[@href='/courses/" + courseid + "/course/']").is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_possible_open_course(self, organization, courseNumber, courseRun):
        '''Get present button View course'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(
                "//a[@href='/courses/" + variables.ID + organization + "+" + courseNumber + "+" + courseRun + "/info'] | "
                "//a[@href='/courses/" + variables.ID + organization + "+" + courseNumber + "+" + courseRun + "/course/']").click()
        except NoSuchElementException:
            result = "0"
        return result

    def get_about_course_text(self, courseId, courseNumber):
        '''Get text dashboard courses'''
        return self.driver.find_element_by_xpath("//section[@aria-labelledby='details-heading-" + courseId + "'] | "
                                                "//section[@aria-labelledby='details-heading-" + courseNumber + "']").text.replace('\n', '; ').lower()

    def get_name(self):
        '''Get text dashboard courses'''
        return self.driver.find_element_by_xpath(self.PATH_USERNAME_FIELD).text

