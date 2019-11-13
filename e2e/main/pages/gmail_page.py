import time
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger

class GmailPage():

    PATH_EMAIL_FIELD = "identifierId"
    PATH_GO_BUTTON = "//span[@class='RveJvd snByac']"
    PATH_PASSWORD_FIELD = "password"
    PATH_GO_BUTTON_SECOND = "//span[@class='RveJvd snByac']"

    PATH_FIRST_MESSAGE = "//div[@class='Cp']/div/table/tbody/tr/td[6]"
    PATH_TIME_MESSAGE = "//span[contains(text(), '0 минут назад')] | //span[contains(text(), '1 минуту назад')]"
    PATH_DELETE_MESSAGE_BUTTON = "//div[@id=':4']/div[2]/div/div/div[2]/div[3]/div"

    PATH_CHANGE_PASSWORD_BUTTON = "//b[contains(text(), 'Change my Password')]"
    PATH_NEW_PASSWORD_FIELD = "//input[@id='new_password1']"
    PATH_CONFIRM_PASSWORD_FIELD = "//input[@id='new_password2']"
    PATH_RESET_PASSWORD_BUTTON = "//button[contains(text(), 'Reset My Password')]"
    PATH_PROMPT_MESSAGE_FIELD = "//div[@id='error-new_password1']"

    def __init__(self, driver, *args, **kwargs):
        super(GmailPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def login(self, email, password):
        '''Login gmail'''
        time.sleep(3)
        self.logger.do_input('Email = "' + email + '"')
        self.driver.find_element_by_id(self.PATH_EMAIL_FIELD).send_keys(email)
        time.sleep(1)
        self.logger.do_click('Go')
        self.driver.find_element_by_xpath(self.PATH_GO_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('Password = "' + password + '"')
        self.driver.find_element_by_name(self.PATH_PASSWORD_FIELD).send_keys(password)
        time.sleep(1)
        self.logger.do_click('Go')
        self.driver.find_element_by_xpath(self.PATH_GO_BUTTON_SECOND).click()
        time.sleep(3)
        self.driver.implicitly_wait(10)

    def delete_all(self):
        '''Delete all'''
        result = "0"
        try:
            if (self.driver.find_element_by_xpath("//a[contains(@href, '" + variables.URL_LMS + "')]").is_enabled()):
                result = "1"
        except:
            pass
        try:
            if(self.driver.find_element_by_xpath(self.PATH_CHANGE_PASSWORD_BUTTON).is_enabled()):
                result = "1"
        except:
            pass
        if (result in "1"):
            self.delete_message()


    def open_first_message(self):
        '''Open first message'''
        try:
            self.logger.do_click('First message on list')
            self.driver.find_element_by_xpath(self.PATH_FIRST_MESSAGE).click()
            time.sleep(5)
        except:
            pass

    def confirm_change_email(self):
        '''Confirm change email'''
        try:
            self.logger.do_click('Confirm')
            self.config.execute_script_click("//a[contains(@href, '" + variables.URL_LMS + "')]")
            time.sleep(3)
        except:
            pass

    def confirm_change_password(self, newPassword, confirmPassword):
        '''Confirm change password'''
        self.logger.do_click('Change my Password')
        self.config.execute_script_click(self.PATH_CHANGE_PASSWORD_BUTTON)
        self.config.switch_window(1)
        self.config.wait_element(self.PATH_NEW_PASSWORD_FIELD)
        self.logger.do_input('New Password = "' + newPassword + '"')
        self.driver.find_element_by_xpath(self.PATH_NEW_PASSWORD_FIELD).send_keys(newPassword)
        self.logger.do_input('Confirm Password = "' + confirmPassword + '"')
        self.driver.find_element_by_xpath(self.PATH_CONFIRM_PASSWORD_FIELD).send_keys(confirmPassword)
        self.logger.do_click('Reset my Password')
        self.config.execute_script_click(self.PATH_RESET_PASSWORD_BUTTON)
        time.sleep(3)

    def delete_message(self):
        '''Delete message'''
        try:
            self.logger.do_click('Delete')
            self.driver.find_element_by_xpath(self.PATH_DELETE_MESSAGE_BUTTON).click()
            time.sleep(3)
        except:
            pass



    def get_text_first_message(self):
        '''Get text first message'''
        return self.driver.find_element_by_xpath(self.PATH_FIRST_MESSAGE).text

    def get_time_message(self):
        '''Get time first message'''
        return self.driver.find_element_by_xpath(self.PATH_TIME_MESSAGE).text

    def get_prompt_message(self):
        '''Get prompt message'''
        return self.driver.find_element_by_xpath(self.PATH_PROMPT_MESSAGE_FIELD).text






