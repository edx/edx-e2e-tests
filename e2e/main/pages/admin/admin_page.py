from e2e.main.conf.logger import Logger
from e2e.main.conf import variables
import time

class AdminPage():

    PATH_HOME_BUTTON = "//a[contains(text(), 'Home')]"

    PATH_CERTIFICATE_GENERATION_BUTTON = "//a[contains(text(), 'Certificate generation configurations')]"
    PATH_ENABLED_BUTTON = "//input[@id='id_enabled']"
    PATH_ADD_BUTTON = "//a[@class='addlink']"

    PATH_CERTIFICATE_HTML_BUTTON = "//a[contains(text(), 'Certificate html view configurations')]"

    PATH_COURSE_MODES_BUTTON = "//a[contains(text(), 'Course modes')]"
    PATH_COURSE_FIELD = "//select[@name='course'] | //input[@id='id_course_id']"
    PATH_MODE_FIELD = "//select[@name='mode_slug']"
    PATH_DISPLAY_NAME_FIELD = "//input[@name='mode_display_name']"
    PATH_SAVE_BUTTON = "//input[@name='_save']"
    PATH_TICK_BUTTON = "//input[@id='action-toggle']"
    PATH_ACTION_FIELD = "//select[@name='action']"
    PATH_GO_BUTTON = "//button[contains(text(), 'Go')]"
    PATH_SUBMIT_BUTTON = "//input[@type='submit']"

    PATH_USERS_BUTTON = "//a[contains(text(), 'Users')]"
    PATH_FILTER_BY_FIELD = "//input[@id='searchbar']"
    PATH_FILTER_BY_BUTTON = "//input[@value='Search']"
    PATH_USERS_LIST = "//form[@id='changelist-form']"

    PATH_COURSE_ENROLLMENTS_BUTTON = "//a[contains(text(), 'Course enrollments')]"

    PATH_LOGOUT_BUTTON = "//a[contains(text(), 'Log out')]"

    def __init__(self, driver, *args, **kwargs):
        super(AdminPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()


    def set_certificate_generation(self, activity):
        '''set certificate generation'''
        self.logger.do_click('Certificate generation')
        self.driver.find_element_by_xpath(self.PATH_CERTIFICATE_GENERATION_BUTTON).click()
        self.logger.do_click('Add certificate')
        self.driver.find_element_by_xpath(self.PATH_ADD_BUTTON).click()
        if(activity == variables.STATUS_ON):
            if(self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).is_selected()):
                pass
            else:
                self.logger.do_click('Enabled')
                self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).click()
        elif(activity == variables.STATUS_OFF):
            if (self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).is_selected()):
                self.logger.do_click('Enabled')
                self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).click()
            else:
                pass
        self.logger.do_click('SAVE')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Home')
        self.driver.find_element_by_xpath(self.PATH_HOME_BUTTON).click()
        time.sleep(3)

    def set_certificate_html(self, activity):
        '''set certificate generation'''
        self.logger.do_click('Certificate html')
        self.driver.find_element_by_xpath(self.PATH_CERTIFICATE_HTML_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Add certificate')
        self.driver.find_element_by_xpath(self.PATH_ADD_BUTTON).click()
        if(activity == variables.STATUS_ON):
            if(self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).is_selected()):
                pass
            else:
                self.logger.do_click('Enabled')
                self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).click()
        elif(activity == variables.STATUS_OFF):
            if (self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).is_selected()):
                self.logger.do_click('Enabled')
                self.driver.find_element_by_xpath(self.PATH_ENABLED_BUTTON).click()
            else:
                pass
        self.logger.do_click('SAVE')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Home')
        self.driver.find_element_by_xpath(self.PATH_HOME_BUTTON).click()
        time.sleep(3)

    def open_course_modes(self):
        '''Open Course modes'''
        self.logger.do_click('Course modes')
        self.driver.find_element_by_xpath(self.PATH_COURSE_MODES_BUTTON).click()
        time.sleep(1)

    def set_course_modes(self, courseId, mode, displayName):
        '''set certificate generation'''
        self.open_course_modes()
        self.logger.do_click('Add')
        self.driver.find_element_by_xpath(self.PATH_ADD_BUTTON).click()
        self.logger.do_input('Course = "' + courseId + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_FIELD).send_keys(courseId)
        self.logger.do_input('Mode = "' + mode + '"')
        self.driver.find_element_by_xpath(self.PATH_MODE_FIELD).send_keys(mode)
        self.logger.do_input('Display Name = "' + displayName + '"')
        self.driver.find_element_by_xpath(self.PATH_DISPLAY_NAME_FIELD).send_keys(displayName)
        self.logger.do_click('SAVE')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Home')
        self.driver.find_element_by_xpath(self.PATH_HOME_BUTTON).click()
        time.sleep(3)

    def open_users(self):
        '''Open users'''
        self.logger.do_click('Users')
        self.driver.find_element_by_xpath(self.PATH_USERS_BUTTON).click()

    def filter_for_admin(self, email):
        '''Filter users'''
        self.logger.do_input('Search by = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_FILTER_BY_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_FILTER_BY_FIELD).send_keys(email)
        self.logger.do_click('Users')
        self.driver.find_element_by_xpath(self.PATH_FILTER_BY_BUTTON).click()
        time.sleep(1)

    def delete_activity_admin(self, text):
        '''Delete Course Mode'''
        try :
            self.logger.do_click('Tick')
            self.driver.find_element_by_xpath(self.PATH_TICK_BUTTON).click()
            time.sleep(1)
            self.logger.do_input('Search by = "' + text + '"')
            self.driver.find_element_by_xpath(self.PATH_ACTION_FIELD).send_keys(text)
            self.logger.do_click('Go')
            self.driver.find_element_by_xpath(self.PATH_GO_BUTTON).click()
            time.sleep(1)
            self.logger.do_click('Submit')
            self.driver.find_element_by_xpath(self.PATH_SUBMIT_BUTTON).click()
            time.sleep(3)
        except:
            pass
        self.logger.do_click('Home')
        self.driver.find_element_by_xpath(self.PATH_HOME_BUTTON).click()
        time.sleep(3)

    def open_course_enrollments(self):
        '''Open Course modes'''
        self.logger.do_click('Course enrollments')
        self.driver.find_element_by_xpath(self.PATH_COURSE_ENROLLMENTS_BUTTON).click()

    def logout(self):
        '''Logout user'''
        self.logger.do_click('Logout')
        self.driver.find_element_by_xpath(self.PATH_LOGOUT_BUTTON).click()



    def get_users_list(self):
        '''Get users list'''
        return self.driver.find_element_by_xpath(self.PATH_USERS_LIST).text.replace('\n', '; ')


