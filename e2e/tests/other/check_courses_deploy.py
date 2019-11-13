import requests
from selenium.webdriver.common.keys import Keys
from e2e.main.conf import variables
from e2e.main.pages.lms.courses_page import CoursesPage
from e2e.main.pages.login_page import LoginPage
from collections import Counter
from e2e.main.tests.main_class import MainClass


class CheckCoursesDeploy(MainClass):

    def setUp(self):
        super(CheckCoursesDeploy, self).setUp()
        self.login_page = LoginPage(self.driver)
        self.courses_page = CoursesPage(self.driver)

    def test_check_cms(self):
        global line
        driver = self.driver

        # Get File List
        file = open('1.txt', 'r')
        fileList = []
        fileListDouble = []
        for line in file.readlines():
            fileList.append(line.replace('\n', '').replace('https://e-learning.tbs-education.ma/courses/course-v1:Microsoft+', '').replace(" ", "_"))
            text = line.replace('https://e-learning.tbs-education.ma/courses/course-v1:Microsoft+', '')
            fileListDouble.append(text[:text.find("+")])

        # Get Studio List
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        studioList = []
        studioListDouble = []
        x = 1
        for i in range(1, 1000):
            try:
                studioList.append(driver.find_element_by_xpath(
                    "//ul[@class='list-courses courses-list']/li[" + str(x) + "]").
                                  get_attribute("data-course-key").replace('course-v1:Microsoft+', ''))
                text = driver.find_element_by_xpath("//ul[@class='list-courses courses-list']/li[" + str(x) + "]").get_attribute("data-course-key").replace('course-v1:Microsoft+', '')
                studioListDouble.append(text[:text.find("+")])
                x = x + 1
            except:
                break

        # Get result including
        checkList = set(fileList) - set(studioList)
        checkStudio = set(studioList) - set(fileList)
        print("Course doesn't present in studio:")
        print()
        print('\n'.join(checkList))
        print("Course doesn't present in list:")
        print()
        print('\n'.join(checkStudio))

        # Get result double
        print("Double courses in list:")
        checkListDouble = [k for k, v in Counter(fileListDouble).items() if v > 1]
        print('\n'.join(checkListDouble))
        print("Double courses in Studio:")
        print()
        checkStudioDouble = [k for k, v in Counter(studioListDouble).items() if v > 1]
        print('\n'.join(checkStudioDouble))
        print('Test is END')



    def test_check_lms(self):
        driver = self.driver

        # Get File List
        file = open('2.txt', 'r')
        fileList = []
        fileListDouble = []
        for line in file.readlines():
            fileList.append(line.replace('\n', '').replace(" ", "_").replace('https://e-learning.tbs-education.ma/courses/course-v1:Microsoft+', ''))
            text = line.replace('https://e-learning.tbs-education.ma/courses/course-v1:Microsoft+', '')
            fileListDouble.append(text[:text.find("+")])

        # Get LMS List
        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        driver.find_element_by_xpath(self.courses_page.PATH_COURSES_BUTTON).click()
        #json
        x = 1
        lmsList = []
        lmsListDouble = []

        for i in range(1, 500):
            driver.find_element_by_xpath(self.courses_page.PATH_COURSES_BUTTON).send_keys(Keys.PAGE_DOWN)

        for i in range(1, 1000):
            try:
                lmsList.append(driver.find_element_by_xpath(
                    "//div[@class='courses']/ul/li[" + str(x) + "]/article/a").
                                  get_attribute('href').replace('http://e-learning.tbs-education.ma/courses/course-v1:Microsoft+', '').replace('/about', ''))
                text = driver.find_element_by_xpath(
                    "//div[@class='courses']/ul/li[" + str(x) + "]/article/a").get_attribute(
                    'href').replace('http://e-learning.tbs-education.ma/courses/course-v1:Microsoft+', '')
                lmsListDouble.append(text[:text.find("+")])
                x = x + 1
            except:
                break

        print(fileList)
        print(fileListDouble)
        print(lmsList)
        print(lmsListDouble)

        # Get result including
        checkList = set(fileList) - set(lmsList)
        checkLms = set(lmsList) - set(fileList)
        print("Course doesn't present in LMS:")
        print()
        print('\n'.join(checkList))
        print("Course doesn't present in list:")
        print()
        print('\n'.join(checkLms))

        # Get result double
        print("Double courses in list:")
        checkListDouble = [k for k, v in Counter(fileListDouble).items() if v > 1]
        print('\n'.join(checkListDouble))
        print("Double courses in LMS:")
        print()
        checkStudioDouble = [k for k, v in Counter(lmsListDouble).items() if v > 1]
        print('\n'.join(checkStudioDouble))
        print('Test is END')