import time
from selenium.webdriver.common.keys import Keys
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger

class AccountPage():

    PATH_DROP_DOWN_BUTTON = "//div[@class='toggle-user-dropdown'] | //button[@class='dropdown'] | " \
                            "//li[@class='nav-item nav-account-user']/h3/span[2] | //button[@class='user-dropdown']/span[2] | " \
                            "//button[@class='menu-button button-more has-dropdown js-dropdown-button']/span"
    PATH_ACCOUNT_BUTTON = "//a[contains(text(), 'Account')]"

    PATH_USERNAME_FIELD = "//span[@id='u-field-value-username']"
    PATH_FULL_NAME_FIELD = "//input[@id='field-input-name']"
    PATH_EMAIL_FIELD = "//input[@id='field-input-email']"
    PATH_RESET_PASSWORD_BUTTON = "//button[@id='u-field-link-password']"
    PATH_AGE_FIELD = "//select[@id='u-field-select-year_of_birth']"
    PATH_REGION_FIELD = "//select[@id='u-field-select-country']"
    PATH_TIME_ZOON_FIELD = "//select[@id='u-field-select-time_zone']"
    PATH_EDUCATION_FIELD = "//select[@id='u-field-select-level_of_education']"
    PATH_GENDER_FIELD = "//select[@id='u-field-select-gender']"
    PATH_PREFERRED_LANGUAGE_FIELD = "//select[@id='u-field-select-language_proficiencies']"
    PATH_TWITTER_FIELD = "//input[@id='field-input-social_links_twitter']"
    PATH_FACEBOOK_FIELD = "//input[@id='field-input-social_links_facebook']"
    PATH_LINKEDIN_FIELD = "//input[@id='field-input-social_links_linkedin']"
    PATH_ALL_PAGE_TEXT = "//div[@id='aboutTabSections-tabpanel']"

    def __init__(self, driver, *args, **kwargs):
        super(AccountPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_account(self):
        '''Open Account'''
        self.logger.do_click('Drop down')
        self.driver.find_element_by_xpath(self.PATH_DROP_DOWN_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Account')
        self.config.wait_element(self.PATH_ACCOUNT_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_ACCOUNT_BUTTON).click()
        time.sleep(3)

    def input_full_name(self, name):
        '''Input full name'''
        self.logger.do_input('Full name = "' + name + '"')
        self.driver.find_element_by_xpath(self.PATH_FULL_NAME_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_FULL_NAME_FIELD).send_keys(name)
        self.driver.find_element_by_xpath(self.PATH_FULL_NAME_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)

    def input_email(self, email):
        '''Input email'''
        self.logger.do_input('Email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FIELD).send_keys(email)
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)

    def click_reset_password(self):
        '''Input email'''
        self.logger.do_click('Reset Your Password')
        self.driver.find_element_by_xpath(self.PATH_RESET_PASSWORD_BUTTON).click()
        time.sleep(3)

    def input_age(self, value):
        '''Input age'''
        self.logger.do_click('Year')
        self.driver.find_element_by_xpath(self.PATH_AGE_FIELD).click()
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def input_region(self, value):
        '''Input region'''
        self.logger.do_click('Region')
        self.driver.find_element_by_xpath(self.PATH_REGION_FIELD).click()
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def input_time_zoon(self, value):
        '''Input time zoon'''
        self.logger.do_click('Time zoon')
        self.driver.find_element_by_xpath(self.PATH_TIME_ZOON_FIELD).click()
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def input_education(self, value):
        '''Input education'''
        self.logger.do_click('Education')
        self.driver.find_element_by_xpath(self.PATH_EDUCATION_FIELD).click()
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def input_gender(self, value):
        '''Input gender'''
        self.logger.do_click('gender')
        self.driver.find_element_by_xpath(self.PATH_GENDER_FIELD).click()
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def input_preferred_language(self, value):
        '''Input preferred language'''
        self.logger.do_click('preferred language')
        self.driver.find_element_by_xpath(self.PATH_PREFERRED_LANGUAGE_FIELD).click()
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        time.sleep(3)

    def input_twitter(self, value):
        '''Input twitter'''
        self.logger.do_input('Twitter = "' + value + '"')
        self.driver.find_element_by_xpath(self.PATH_TWITTER_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_TWITTER_FIELD).send_keys(value)
        self.driver.find_element_by_xpath(self.PATH_TWITTER_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)

    def input_facebook(self, value):
        '''Input facebook'''
        self.logger.do_input('facebook = "' + value + '"')
        self.driver.find_element_by_xpath(self.PATH_FACEBOOK_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_FACEBOOK_FIELD).send_keys(value)
        self.driver.find_element_by_xpath(self.PATH_FACEBOOK_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)

    def input_linkedin(self, value):
        '''Input linkedin'''
        self.logger.do_input('linkedin = "' + value + '"')
        self.driver.find_element_by_xpath(self.PATH_LINKEDIN_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_LINKEDIN_FIELD).send_keys(value)
        self.driver.find_element_by_xpath(self.PATH_LINKEDIN_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)





    def get_text_all_page(self):
        '''Get email'''
        return self.driver.find_element_by_xpath(self.PATH_ALL_PAGE_TEXT).text.replace('\n', '; ')

    def get_username(self):
        '''Get username'''
        return self.driver.find_element_by_xpath(self.PATH_USERNAME_FIELD).text

    def get_full_name(self):
        '''Get full name'''
        return self.driver.find_element_by_xpath(self.PATH_FULL_NAME_FIELD).get_attribute("value")

    def get_email(self):
        '''Get email'''
        return self.driver.find_element_by_xpath(self.PATH_EMAIL_FIELD).get_attribute("value")

    def get_region(self):
        '''Get region'''
        return self.driver.find_element_by_xpath(self.PATH_REGION_FIELD).get_attribute("value")

    def get_time_zoon(self):
        '''Get time zoon'''
        return self.driver.find_element_by_xpath(self.PATH_TIME_ZOON_FIELD).get_attribute("value")

    def get_education(self):
        '''Get education'''
        return self.driver.find_element_by_xpath(self.PATH_EDUCATION_FIELD).get_attribute("value")

    def get_gender(self):
        '''Get gender'''
        return self.driver.find_element_by_xpath(self.PATH_GENDER_FIELD).get_attribute("value")

    def get_preferred_language(self):
        '''Get preferred language'''
        return self.driver.find_element_by_xpath(self.PATH_PREFERRED_LANGUAGE_FIELD).get_attribute("value")