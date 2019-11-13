import time
import requests
from lxml import html
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables
from e2e.main.pages.lms.dashboard_page import DashboardPage

class LoginPage():

    PATH_LOGIN_PROMPT = "//ul[@class='message-copy'] | //p[@class='alert alert-danger']"
    PATH_SIGN_IN_BUTTON = "//a[@class='sign-in-btn btn'] | //li[@class='item nav-courseware-01']/a | //a[@class='action action-signin'] | //a[contains(text(), 'Sign in')]"
    PATH_LOGIN_EMAIL_FIELD = "//input[@id='login-email'] | //input[@id='email'] | //input[@id='login'] | //input[@id='id_username']"
    PATH_LOGIN_PASSWORD_FIELD = "//input[@id='login-password'] | //input[@id='password'] | //input[@id='id_password']"
    PATH_LOGIN_BUTTON = "//form[@id='login']/button | //form[@id='login_form']/div/button | //form[@class='oe_login_form']/div[3]/button " \
                        "| //form[@id='login-form']/div[3]/input | //button[@class='action action-primary action-update login-button']"
    PATH_FORGOT_PASSWORD_BUTTON = "//button[@class='forgot-password field-link']"
    PATH_PASSWORD_RESET_EMAIL = "password-reset-email"
    PATH_RESET_PASSWORD_BUTTON = "//button[@class='action action-primary action-update js-reset']"
    PATH_VIEW_SITE_BUTTON = "//a[contains(text(), 'View site')]"
    PATH_LAUNCH_STUDIO_BUTTON = "//a[contains(text(), 'LAUNCH STUDIO')]"
    PATH_LIST_COURSES = "//section[@class='courses']"

    def __init__(self, driver, *args, **kwargs):
        super(LoginPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.dashboard_page = DashboardPage(self.driver)
        self.config = Config(self.driver)



    def input_url(self, platform):
        '''Input url'''
        if (platform == variables.STATUS_CMS):
            if (variables.PROJECT == variables.PROJECT_ASUOSPP):
                url = variables.URL_ADMIN
            else:
                url = variables.URL_CMS
        elif (platform == variables.STATUS_LMS):
            url = variables.URL_LMS
        else:
            url = variables.URL_ADMIN

        self.logger.do_input('URL = "' + url + '"')
        self.driver.get(url)
        time.sleep(3)
        self.driver.implicitly_wait(10)

    def click_sign_in_button(self, platform):
        '''Click button Sign In'''
        if(variables.PROJECT not in (variables.PROJECT_ASUOSPP)):
            if(platform != variables.STATUS_ADMIN):
                self.logger.do_click('Sign in')
                self.config.wait_element(self.PATH_SIGN_IN_BUTTON)
                self.driver.find_element_by_xpath(self.PATH_SIGN_IN_BUTTON).click()
                time.sleep(3)

    def input_email(self, email):
        '''Input password'''
        self.logger.do_input('Email = "' + email + '"')
        self.config.wait_element(self.PATH_LOGIN_EMAIL_FIELD)
        self.driver.find_element_by_xpath(self.PATH_LOGIN_EMAIL_FIELD).send_keys(email)
        time.sleep(1)

    def input_password(self, password):
        '''Input password'''
        self.logger.do_input('Password = "' + password + '"')
        self.driver.find_element_by_xpath(self.PATH_LOGIN_PASSWORD_FIELD).send_keys(password)
        time.sleep(1)

    def click_login_button(self):
        '''Click login button'''
        self.logger.do_click('Login')
        self.driver.find_element_by_xpath(self.PATH_LOGIN_BUTTON).click()
        time.sleep(3)
        try:
            self.config.wait_element(self.dashboard_page.PATH_LOGIN_WAIT)
        except:
            pass

    def login(self, email, password, platform):
        '''Logging user'''

        '''Set users email'''
        if(platform == variables.STATUS_ADMIN):
            email = variables.LOGIN_EMAIL_ADMIN
        elif(platform == variables.STATUS_CMS and variables.PROJECT == variables.PROJECT_ASUOSPP and
             email not in variables.LOGIN_EMAIL_FIRST or platform == variables.STATUS_CMS and variables.PROJECT == variables.PROJECT_LETSTUDY and
             email not in variables.LOGIN_EMAIL_FIRST):
            email = variables.LOGIN_EMAIL_ADMIN

        '''Set URL'''
        if(variables.PROJECT == variables.PROJECT_ASUOSPP and platform == variables.STATUS_CMS and email == variables.LOGIN_EMAIL_FIRST):
            self.config.input_url(variables.URL_LMS)
        else:
            self.input_url(platform)

        if(platform in variables.STATUS_CMS and variables.PROJECT in variables.PROJECT_LETSTUDY):
            pass
        else:
            self.click_sign_in_button(platform)
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()

        '''Go to CMS from LMS for ASU OSPP'''
        if (variables.PROJECT == variables.PROJECT_ASUOSPP and platform == variables.STATUS_CMS):
            if(email not in variables.LOGIN_EMAIL_FIRST):
                self.logger.do_click('View site')
                self.driver.find_element_by_xpath(self.PATH_VIEW_SITE_BUTTON).click()
                time.sleep(5)
            self.logger.do_click('Launch Studio')
            self.driver.find_element_by_xpath(self.PATH_LAUNCH_STUDIO_BUTTON).click()
            time.sleep(5)

        if (variables.PROJECT == variables.PROJECT_LETSTUDY and platform == variables.STATUS_CMS):
            if(email not in variables.LOGIN_EMAIL_FIRST):
                self.logger.do_click('View site')
                self.driver.find_element_by_xpath(self.PATH_VIEW_SITE_BUTTON).click()
                time.sleep(5)

        '''Open enrolled courses for E4H'''
        if (platform == variables.STATUS_LMS):
            if(variables.PROJECT in (variables.PROJECT_E4H)):
                try:
                    self.dashboard_page.open_enrolled_courses()
                except NoSuchElementException:
                    pass

    def set_leng(self, email, platform):
        if(variables.PROJECT in (variables.PROJECT_ASUSGAB)):
            self.config.input_url(variables.URL_LENG)
            self.driver.find_element_by_xpath("//input[@name='preview_language']").send_keys("en")
            self.driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
            if (variables.PROJECT == variables.PROJECT_ASUOSPP and platform == variables.STATUS_CMS and email == variables.LOGIN_EMAIL_FIRST):
                self.config.input_url(variables.URL_LMS)
            else:
                self.input_url(platform)


    def forgot_password(self, email):
        '''Reactivate password'''
        self.logger.do_click('Sign in')
        self.driver.find_element_by_xpath(self.PATH_SIGN_IN_BUTTON).click()
        self.logger.do_click('Forgot password')
        self.driver.find_element_by_xpath(self.PATH_FORGOT_PASSWORD_BUTTON).click()
        self.logger.do_input('Email = "' + email + '"')
        self.driver.find_element_by_id(self.PATH_PASSWORD_RESET_EMAIL).send_keys(email)
        self.logger.do_click('Reset my password')
        self.driver.find_element_by_xpath(self.PATH_RESET_PASSWORD_BUTTON).click()




    def get_list_courses(self):
        '''Get list courses'''
        x = 1
        lmsList = []
        for i in range(1, 200):
            page = requests.get(variables.URL_LMS)
            tree = html.fromstring(page.content)
            trs1 = tree.xpath("//ul[@class='courses-listing']/li[" + str(x) + "]/article")
            for tr in trs1:
                lmsList.append(tr.attrib.get('id'))
            x = x + 1
        return lmsList

    def get_password_type(self):
        '''Get text of prompt messages on logging page'''
        return self.driver.find_element_by_xpath(self.PATH_LOGIN_PASSWORD_FIELD).get_attribute('type')

    def get_text_prompt_message(self):
        '''Get text of prompt messages on logging page'''
        return self.driver.find_element_by_xpath(self.PATH_LOGIN_PROMPT).text

    def get_view_logIn_button(self):
        '''Get view login button'''
        result = '1'
        try:
            self.driver.find_element_by_xpath(self.PATH_LOGIN_BUTTON).is_enabled()
        except NoSuchElementException:
            result = '0'
        return result

