import time
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger

class ProfilePage():
    PATH_DROP_DOWN_BUTTON = "//div[@class='toggle-user-dropdown'] | //button[@class='dropdown'] | " \
                            "//li[@class='nav-item nav-account-user']/h3/span[2] | //button[@class='user-dropdown']/span[2] | " \
                            "//button[@class='menu-button button-more has-dropdown js-dropdown-button']/span"
    PATH_PROFILE_BUTTON = "//a[contains(text(), 'Profile')]"

    PATH_PROFILE_VISIBILITY_FIELD = "//select[@id='u-field-select-account_privacy']"
    PATH_SAVE_BUTTON = "//span[contains(text(), 'Save')]"
    PATH_MY_NAME_TEXT = "//span[@id='u-field-value-username']"

    PATH_TWITTER_PROFILE_BUTTON = "//span[@class='icon fa fa-twitter-square']"
    PATH_FACEBOOK_PROFILE_BUTTON = "//span[@class='icon fa fa-facebook-square']"
    PATH_LINKEDIN_PROFILE_BUTTON = "//span[@class='icon fa fa-linkedin-square']"
    PATH_TO_SHOWN_LOCATION_BUTTON = "//div[@class='u-field u-field-dropdown u-field-country editable-toggle mode-display'] | " \
                                    "//div[@class='u-field u-field-dropdown u-field-country editable-toggle mode-placeholder']"
    PATH_LOCATION_BUTTON = "//select[@id='u-field-select-country']"
    PATH_TO_SHOWN_LANGUAGE_BUTTON = "//div[@class='u-field u-field-dropdown u-field-language_proficiencies editable-toggle mode-display'] | " \
                                    "//div[@class='u-field u-field-dropdown u-field-language_proficiencies editable-toggle mode-placeholder']"
    PATH_LANGUAGE_BUTTON = "//select[@id='u-field-select-language_proficiencies']"

    PATH_ABOUT_ME_BUTTON = "//span[@id='u-field-title-bio']"
    PATH_ABOUT_ME_FIELD = "//div[@id='u-field-value-bio']"
    PATH_EXPLORE_COURSES_BUTTON = "//span[@class='icon fa fa-search']"
    PATH_PROFILE_TEXT = "//div[@class='profile profile-self']"
    PATH_TWITTER_LOGIN_BUTTON = "//span[contains(text(), ' Log in')]"
    PATH_FACEBOOK_LOGIN_BUTTON = "//label[@id='loginbutton']/input"
    PATH_LINKEDIN_LOGIN_BUTTON = "//a[contains(text(), 'Sign in')]"

    def __init__(self, driver, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_profile(self):
        '''Open Account'''
        self.logger.do_click('Drop down')
        self.driver.find_element_by_xpath(self.PATH_DROP_DOWN_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Profile')
        self.config.wait_element(self.PATH_PROFILE_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_PROFILE_BUTTON).click()
        time.sleep(3)

    def set_profile_visibility(self, value):
        '''Set profile visibility'''
        try:
            self.logger.do_click('Visibility = "' + value + '"')
            self.driver.find_element_by_xpath(self.PATH_PROFILE_VISIBILITY_FIELD).send_keys(value)
            self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
            time.sleep(3)
            self.driver.find_element_by_xpath(self.PATH_MY_NAME_TEXT).click()
        except:
            pass

    def open_twitter_profile(self):
        '''Open Twitter profile'''
        self.logger.do_click('Twitter profile')
        self.driver.find_element_by_xpath(self.PATH_TWITTER_PROFILE_BUTTON).click()
        time.sleep(3)

    def open_facebook_profile(self):
        '''Open Facebook profile'''
        self.logger.do_click('Facebook profile')
        self.driver.find_element_by_xpath(self.PATH_FACEBOOK_PROFILE_BUTTON).click()
        time.sleep(3)

    def open_linkedin_profile(self):
        '''Open Linkedin profile'''
        self.logger.do_click('Linkedin profile')
        self.driver.find_element_by_xpath(self.PATH_LINKEDIN_PROFILE_BUTTON).click()
        time.sleep(3)

    def input_location(self, value):
        '''Input location'''
        self.logger.do_click('Location')
        self.driver.find_element_by_xpath(self.PATH_TO_SHOWN_LOCATION_BUTTON).click()
        self.driver.find_element_by_xpath(self.PATH_LOCATION_BUTTON).click()
        time.sleep(1)
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        self.driver.find_element_by_xpath(self.PATH_MY_NAME_TEXT).click()
        time.sleep(1)

    def input_language(self, value):
        '''Input language'''
        self.logger.do_click('Language')
        self.driver.find_element_by_xpath(self.PATH_TO_SHOWN_LANGUAGE_BUTTON).click()
        self.driver.find_element_by_xpath(self.PATH_LANGUAGE_BUTTON).click()
        time.sleep(1)
        self.logger.do_click(value)
        self.driver.find_element_by_xpath("//option[contains(text(), '" + value + "')]").click()
        self.driver.find_element_by_xpath(self.PATH_MY_NAME_TEXT).click()
        time.sleep(1)

    def input_about_me(self, value):
        '''Input about me'''
        self.logger.do_click('Language')
        self.driver.find_element_by_xpath(self.PATH_ABOUT_ME_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('About me = "' + value + '"')
        self.config.execute_script_input(self.PATH_ABOUT_ME_FIELD, value)
        self.driver.find_element_by_xpath(self.PATH_MY_NAME_TEXT).click()
        time.sleep(1)

    def click_explore_new_courses(self):
        '''Click explore new courses'''
        self.logger.do_click('explore new courses')
        self.driver.find_element_by_xpath(self.PATH_EXPLORE_COURSES_BUTTON).click()
        time.sleep(3)



    def get_profile_text(self):
        '''Get profile text'''
        return self.driver.find_element_by_xpath(self.PATH_PROFILE_TEXT).text.replace('\n', '; ')

    def get_activity_profilele_disabled(self):
        '''Get activity profile disabled'''
        return self.driver.find_element_by_xpath(self.PATH_PROFILE_VISIBILITY_FIELD).get_attribute("disabled")

    def get_possible_change_profile_visibility(self, value):
        '''Get possible change profile visibility'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_PROFILE_VISIBILITY_FIELD).send_keys(value)
        except:
            result = "0"
        return result

    def get_twitter_profile_present(self):
        '''Get twitter profile present'''
        return self.driver.find_element_by_xpath(self.PATH_TWITTER_LOGIN_BUTTON).text.lower()

    def get_facebook_profile_present(self):
        '''Get facebook profile present'''
        return self.driver.find_element_by_xpath(self.PATH_FACEBOOK_LOGIN_BUTTON).get_attribute("value").lower()

    def get_linkedin_profile_present(self):
        '''Get linkedin profile present'''
        return self.driver.find_element_by_xpath(self.PATH_LINKEDIN_LOGIN_BUTTON).text.lower()
