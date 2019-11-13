from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
import time

class SysadminPage():

    PATH_SYSADMIN_BUTTON = "//a[contains(text(), 'Sysadmin')]"

    PATH_USERS_BUTTON = "//a[contains(text(), 'Users')]"
    PATH_EMAIL_FIELD = "//input[@name='student_uname']"
    PATH_FULL_NAME_FIELD = "//input[@name='student_fullname']"
    PATH_PASSWORD_FIELD = "//input[@name='student_password']"
    PATH_CREATE_USER_BUTTON = "//button[contains(text(), 'Create user')]"
    PATH_DELETE_USER_BUTTON = "//button[contains(text(), 'Delete user')]"

    PATH_COURSES_BUTTON = "//a[contains(@href, '/sysadmin/courses')]"
    PATH_COURSE_ID_FIELD = "//input[@name='course_id']"
    PATH_DELETE_COURSE_BUTTON = "//button[contains(text(), 'Delete course from site')]"
    PATH_COURSES = "//table[@class='stat_table']"

    def __init__(self, driver, *args, **kwargs):
        super(SysadminPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_users(self):
        '''Open Users'''
        self.logger.do_click('Sysadmin')
        if (variables.PROJECT not in (variables.PROJECT_ASUOSPP)):
            self.driver.find_element_by_xpath(self.PATH_SYSADMIN_BUTTON).click()
            time.sleep(3)
        else:
            self.config.input_url(variables.URL_SYSADMIN)
        self.logger.do_click('Users')
        self.driver.find_element_by_xpath(self.PATH_USERS_BUTTON).click()
        time.sleep(3)

    def add_user(self, email, name, password):
        '''Add user'''
        self.logger.do_input('Email or username = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Full Name = "' + name + '"')
        self.driver.find_element_by_xpath(self.PATH_FULL_NAME_FIELD).send_keys(name)
        self.logger.do_input('Password = "' + password + '"')
        self.driver.find_element_by_xpath(self.PATH_PASSWORD_FIELD).send_keys(password)
        self.logger.do_click('Create user')
        self.driver.find_element_by_xpath(self.PATH_CREATE_USER_BUTTON).click()
        time.sleep(3)

    def delete_user(self, email):
        '''Delete user'''
        self.logger.do_input('Email or username = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FIELD).send_keys(email)
        self.logger.do_click('Delete user')
        self.driver.find_element_by_xpath(self.PATH_DELETE_USER_BUTTON).click()
        time.sleep(3)

    def open_courses(self):
        '''Open Courses'''
        self.logger.do_click('Sysadmin')
        if(variables.PROJECT in (variables.PROJECT_ASUOSPP)):
            self.config.input_url(variables.URL_SYSADMIN)
        else:
            self.driver.find_element_by_xpath(self.PATH_SYSADMIN_BUTTON).click()

        time.sleep(1)
        self.logger.do_click('Courses')
        self.driver.find_element_by_xpath(self.PATH_COURSES_BUTTON).click()
        time.sleep(3)

    def delete_course(self, id):
        '''Delete course'''
        self.logger.do_input('Course id = "' + id + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_ID_FIELD).send_keys(id)
        self.logger.do_click('Delete course from site')
        self.driver.find_element_by_xpath(self.PATH_DELETE_COURSE_BUTTON).click()
        time.sleep(1)
        self.driver.implicitly_wait(20)


    def delete_created_courses(self):
        self.config.wait_element(self.PATH_COURSES)
        textList = self.get_courses_list_text().split(" ")
        countTextList = len(textList)
        number = 0
        courseList = ""
        for i in range(number, countTextList):
            if "course-v1:" + variables.ORGANIZATION_FOR_DELETE in textList[number]:
                courseList = courseList + textList[number]
            number = number + 1

        number = 0
        courseList = courseList.split(";")
        countCoursList = len(courseList)
        for i in range(number, countCoursList):
            self.delete_course(courseList[number])
            number = number + 1
            self.driver.implicitly_wait(30)




    def get_courses_list_text(self):
        return self.driver.find_element_by_xpath(self.PATH_COURSES).text.replace('\n', '; ')