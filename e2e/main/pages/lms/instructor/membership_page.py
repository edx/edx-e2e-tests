import time
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables

class MembershipPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_MEMBERSHIP_BUTTON = "//button[contains(text(), 'Membership')]"

    PATH_USER_EMAIL_FIELD = "//textarea[@name='student-ids']"
    PATH_REASON_FIELD = "//textarea[@name='reason-field']"
    PATH_BETTA_TESTER_EMAIL_FIELD = "//textarea[@name='student-ids-for-beta']"

    PATH_AUTO_ENROLL_BUTTON = "//input[@id='auto-enroll']"
    PATH_NOTIFY_USER_BUTTON = "//input[@id='email-students']"
    PATH_AUTO_ENROLL_BETA_BUTTON = "//input[@name='auto-enroll-beta']"
    PATH_NOTIFY_USER_BETA_BUTTON = "//input[@name='email-students-beta']"

    PATH_ENROLL_BUTTON = "//input[@value='Enroll']"
    PATH_UNENROLL_BUTTON = "//input[@value='Unenroll']"
    PATH_ADD_BETA_TESTERS_BUTTON = "//input[@value='Add beta testers']"
    PATH_REMOVE_BETA_TESTERS_BUTTON = "//input[@value='Remove beta testers']"

    PATH_TEAM_ROLE_FIELD = "//select[@id='member-lists-selector']"
    PATH_EMAIL_TEAM_MANAGEMENT_FIELD = "//div[@class='auth-list-container active']/div/div[4]/label/input"
    PATH_ADD_TEAM_MANAGEMENT_BUTTON = "//div[@class='auth-list-container active']/div/div[4]/input"
    PATH_TEAM_MANAGEMENT_TABLE = "//div[@class='auth-list-container active']/div/div[3]"
    PATH_ROLE_TO_ADD_FIELD = "//select[@id='member-lists-selector']"

    def __init__(self, driver, *args, **kwargs):
        super(MembershipPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_membership(self):
        '''Open membership'''
        self.logger.do_click('Instructor')
        self.config.execute_script_click(self.PATH_INSTRUCTOR_BUTTON)
        time.sleep(1)
        self.config.switch_window(0)
        time.sleep(1)
        self.logger.do_click('Membership')
        self.driver.find_element_by_xpath(self.PATH_MEMBERSHIP_BUTTON).click()
        time.sleep(1)

    def enroll_user(self, email, reason, activity, auto, notify):
        '''Enroll/Unenroll user'''
        self.logger.do_input('Email Addresses/Usernames = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_USER_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_USER_EMAIL_FIELD).send_keys(email)
        if(variables.VERSION in variables.VERSION_HAWTHORN):
            self.logger.do_input('Reason = "' + reason + '"')
            self.driver.find_element_by_xpath(self.PATH_REASON_FIELD).clear()
            self.driver.find_element_by_xpath(self.PATH_REASON_FIELD).send_keys(reason)

        if(auto == True):
            if(self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BUTTON).is_selected()):
                pass
            else:
                self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BUTTON).click()
        else:
            if (self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BUTTON).is_selected()):
                self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BUTTON).click()
            else:
                pass
        if (notify == True):
            if (self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BUTTON).is_selected()):
                pass
            else:
                self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BUTTON).click()
        else:
            if (self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BUTTON).is_selected()):
                self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BUTTON).click()
            else:
                pass
        if(activity == variables.STATUS_ENROLL):
            self.logger.do_click('Enroll')
            self.driver.find_element_by_xpath(self.PATH_ENROLL_BUTTON).click()
        elif(activity == variables.STATUS_UNENROLL):
            self.logger.do_click('Unenroll')
            self.driver.find_element_by_xpath(self.PATH_UNENROLL_BUTTON).click()
        time.sleep(1)

    def enroll_beta_tester(self, email, activity, auto, notify):
        '''Enroll/Unenroll beta tester'''
        self.logger.do_input('Email Addresses/Usernames = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_BETTA_TESTER_EMAIL_FIELD).send_keys(email)
        if(auto == True):
            if(self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BETA_BUTTON).is_selected()):
                pass
            else:
                self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BETA_BUTTON).click()
        else:
            if (self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BETA_BUTTON).is_selected()):
                self.driver.find_element_by_xpath(self.PATH_AUTO_ENROLL_BETA_BUTTON).click()
                self.driver.find_element_by_xpath(self.PATH_BETTA_TESTER_EMAIL_FIELD).click()
            else:
                pass
        if (notify == True):
            if (self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BETA_BUTTON).is_selected()):
                pass
            else:
                self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BETA_BUTTON).click()
        else:
            if (self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BETA_BUTTON).is_selected()):
                self.driver.find_element_by_xpath(self.PATH_NOTIFY_USER_BETA_BUTTON).click()
            else:
                pass
        if(activity == variables.STATUS_ENROLL):
            self.logger.do_click('Enroll')
            self.driver.find_element_by_xpath(self.PATH_ADD_BETA_TESTERS_BUTTON).click()
        elif(activity == variables.STATUS_UNENROLL):
            self.logger.do_click('Unenroll')
            self.driver.find_element_by_xpath(self.PATH_REMOVE_BETA_TESTERS_BUTTON).click()
        time.sleep(1)

    def set_role(self, role):
        '''Set role'''
        self.logger.do_input('Select a course team role: = "' + role + '"')
        self.driver.find_element_by_xpath(self.PATH_TEAM_ROLE_FIELD).send_keys(role)
        time.sleep(1)

    def add_new_role(self, email):
        '''Add new role'''
        self.logger.do_input('Enter username or email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_EMAIL_TEAM_MANAGEMENT_FIELD).send_keys(email)
        self.logger.do_click('Add')
        self.driver.find_element_by_xpath(self.PATH_ADD_TEAM_MANAGEMENT_BUTTON).click()
        time.sleep(3)

    def delete_new_role(self, email):
        '''Delete new role'''
        result = "1"
        try:
            assert (email in self.driver.find_element_by_xpath(self.PATH_TEAM_MANAGEMENT_TABLE).text)
        except:
            result = "0"

        if(result == "1"):
            self.logger.do_click('Delete')
            self.driver.find_element_by_xpath("//td[contains(text(), '" + email + "')]/following-sibling::td/div").click()
            time.sleep(3)

    def delete_all_roles(self):
        '''Delete all roles'''
        self.set_role(variables.ROLE_STAFF)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)

        self.set_role(variables.ROLE_ADMIN)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)

        self.set_role(variables.ROLE_BETA_TESTERS)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)

        self.set_role(variables.ROLE_DISCUSSION_ADMINS)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)

        self.set_role(variables.ROLE_DISCUSSION_MODERATORS)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)

        self.set_role(variables.ROLE_DISCUSSION_COMMUNITY_TAS)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)

        self.set_role(variables.ROLE_GROUP_COMMUNITY_TA)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)

        self.set_role(variables.ROLE_COMMUNITY_TA)
        self.delete_new_role(variables.LOGIN_EMAIL_FIRST)
        self.delete_new_role(variables.LOGIN_EMAIL_SECOND)



    def get_possible_add_new_role(self):
        '''Get possible add new role'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_ADD_TEAM_MANAGEMENT_BUTTON).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_team_management(self):
        '''Get team management'''
        return self.driver.find_element_by_xpath(self.PATH_TEAM_MANAGEMENT_TABLE).text.replace('\n', '; ')

    def get_role_to_add(self):
        '''Get role to add'''
        return self.driver.find_element_by_xpath(self.PATH_ROLE_TO_ADD_FIELD).text.replace('\n', '; ')

