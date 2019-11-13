import time
from e2e.main.conf.logger import Logger
from e2e.main.conf.config import Config
import random
from e2e.main.conf import variables
from e2e.main.pages.login_page import LoginPage

class RegistrationPage():

    PATH_REGISTER_BUTTON = "//li[@class='item nav-global-04']/a | //a[@class='register-btn btn']"
    PATH_EMAIL_FIELD = "register-email"
    PATH_FULL_NAME_FIELD = "register-name"
    PATH_USERNAME_FIELD = "register-username"
    PATH_PASSWORD_FIELD = "register-password"
    PATH_AGREE_BUTTON = "register-honor_code"
    PATH_CREATE_ACCOUNT_BUTTON = "//button[@class='action action-primary action-update js-register register-button']"
    PATH_PROMPT_MESSAGE = "//ul[@class ='message-copy']"

    PATH_AGREE_TERMS_SERVICE_BUTTON = "//input[@id ='register-terms_of_service']"
    PATH_AGREE_HONOR_CODE_BUTTON = "//input[@id ='register-honor_code']"

    def __init__(self, driver, *args, **kwargs):
        super(RegistrationPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.login_page = LoginPage(self.driver)

    def getEmail(self):
        '''Get random email'''
        return variables.EMAIL_FOR_CREATE + str(random.randint(1, 100000)) + '@gmail.com'

    def getUsername(self):
        '''Get random username'''
        return variables.NAME_FOR_CREATE + str(random.randint(1, 100000))

    def clickButtonRegistration(self):
        '''Click button registration'''
        self.logger.do_click('Register')
        self.driver.find_element_by_xpath(self.PATH_REGISTER_BUTTON).click()

    def inputPassword(self, password):
        '''Input password'''
        self.logger.do_input('Password = "' + password + '"')
        self.driver.find_element_by_id(self.PATH_PASSWORD_FIELD).send_keys(password)



    def registration(self, email, fullName, username, password, agree, platform):
        '''Registration'''
        self.login_page.input_url(platform)
        self.clickButtonRegistration()
        self.logger.do_input('Email = "' + email + '"')
        self.driver.find_element_by_id(self.PATH_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Full name = "' + fullName + '"')
        self.driver.find_element_by_id(self.PATH_FULL_NAME_FIELD).send_keys(fullName)
        self.logger.do_input('Public username = "' + username + '"')
        self.driver.find_element_by_id(self.PATH_USERNAME_FIELD).send_keys(username)
        self.inputPassword(password)

        if(agree == True):
            self.logger.do_click("I agree")
            self.driver.find_element_by_id(self.PATH_AGREE_BUTTON).click()

            if (variables.PROJECT == variables.PROJECT_DEMOUNIVERSITY):
                self.logger.do_click("Agree Terms of Service")
                Config.scroll_to_element(self, "xpath", self.PATH_AGREE_TERMS_SERVICE_BUTTON)
                self.driver.find_element_by_xpath(self.PATH_AGREE_TERMS_SERVICE_BUTTON).click()

                self.logger.do_click("Agree Honor Code")
                Config.scroll_to_element(self, "xpath", self.PATH_AGREE_HONOR_CODE_BUTTON)
                self.driver.find_element_by_xpath(self.PATH_AGREE_HONOR_CODE_BUTTON).click()

        self.logger.do_click("Create account")
        Config.scroll_to_element(self, "xpath", self.PATH_CREATE_ACCOUNT_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_CREATE_ACCOUNT_BUTTON).click()
        time.sleep(10)



    def getTextPromptMessage(self):
        '''Get text of prompt messages on logging page'''
        return self.driver.find_element_by_xpath(self.PATH_PROMPT_MESSAGE).text

    def getPasswordType(self):
        '''Get type of password field'''
        return self.driver.find_element_by_id(self.PATH_PASSWORD_FIELD).get_attribute('type')

    def getValueEmail(self):
        '''Get value Email'''
        return self.driver.find_element_by_id(self.PATH_EMAIL_FIELD).get_attribute('value')

    def getValueFullName(self):
        '''Get value Full name'''
        return self.driver.find_element_by_id(self.PATH_FULL_NAME_FIELD).get_attribute('value')

    def getValueUsername(self):
        '''Get value Username'''
        return self.driver.find_element_by_id(self.PATH_USERNAME_FIELD).get_attribute('value')

    def getValuePassword(self):
        '''Get value Password'''
        return self.driver.find_element_by_id(self.PATH_PASSWORD_FIELD).get_attribute('value')
