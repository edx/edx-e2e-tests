import random
import time
from selenium.webdriver.common.keys import Keys
from PIL import ImageGrab
from selenium.webdriver import ActionChains
from e2e.main.conf import variables
from e2e.main.conf.logger import Logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

class Config():

    def __init__(self, driver, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()

    def input_url(self, url):
        '''Input URL'''
        self.driver.get(url)
        self.driver.implicitly_wait(15)


    def execute_script_input(self, path, value):
        '''Script inputL'''
        search_bar = self.driver.find_element_by_xpath(path)
        actions = ActionChains(self.driver)
        actions.click(search_bar)
        actions.click()
        actions.send_keys(Keys.ARROW_LEFT)
        for i in range(1, 500):
            actions.send_keys(Keys.DELETE)
        for i in range(1, 500):
            actions.send_keys(Keys.BACK_SPACE)
        actions.send_keys(value)
        actions.perform()

    def execute_script_click(self, path):
        '''Script click'''
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element_by_xpath(path))

    def get_random(self):
        '''Get instructor name'''
        return str(random.randint(1, 100000))

    def get_course_number(self):
        '''Get instructor name'''
        return variables.FOR_COURSE_NUMBER + str(random.randint(1, 100000))

    def switch_window(self, number):
        x = self.driver.window_handles[number]
        self.driver.switch_to_window(x)
        time.sleep(1)

    def do_screen(self):
        '''Do screen if test has error in assert'''
        number = random.randint(1, 100000)
        img = ImageGrab.grab().convert('RGB')
        img.save(variables.PATH_TO_LIB + '/Screens/Errors/' + self.logger.get_tyme() + ' ErrorScreen_#_' + str(number) + '.jpg')
        print('[' + self.logger.get_tyme() + '][Result]Have got Error, made screen "ErrorScreen_#_' + str(
            number) + '.jpg" by path "' + variables.PATH_TO_LIB + '/Screens/Errors/"')

    def do_assert_true(self, i, y):
        '''Do assert true'''
        print('[' + self.logger.get_tyme() + '][AssertTrue]Value = "' + str(i) + '"; veb = "' + str(y) + '"')
        if(i != y):
            self.do_screen()
        assert (i == y)

    def do_assert_more(self, i, y):
        '''Do assert true'''
        print('[' + self.logger.get_tyme() + '][AssertTrue]Value = "' + str(i) + '"; veb = "' + str(y) + '"')
        if(i < y):
            self.do_screen()
        assert (i > y)

    def do_assert_true_in(self, i, y):
        '''Do assert true'''
        print('[' + self.logger.get_tyme() + '][AssertTrue]Value = "' + str(i) + ' in: ' + str(y) + '"')
        if(str(i) not in str(y)):
            self.do_screen()
        assert (str(i) in str(y))

    def do_assert_false_in(self, i, y):
        '''Do assert true'''
        print('[' + self.logger.get_tyme() + '][AssertFalse]Value = "' + str(i) + '" in: "' + str(y) + '"')
        if(str(i) in str(y)):
            self.do_screen()
        assert (str(i) not in str(y))

    def scroll_to_element(self, type, element):
        '''Scroll to element'''
        actions = ActionChains(self.driver)
        if(type=="xpath"):
            actions.move_to_element(self.driver.find_element_by_xpath(element)).perform()

    def wait_for_ajax(self, xpath, timeout=10):
        wait = WebDriverWait(self.driver, timeout=int(timeout))
        message = "Element '%s' was not visible in %s second(s)." % (xpath, str(timeout))
        wait.until(lambda driver: driver.find_element_by_xpath(xpath).is_displayed()
                                  and driver.execute_script("return $.active") == 0, message=message)

    def refresh_page(self):
        self.driver.refresh()
        time.sleep(3)

    def wait_element(self, path):
        wait = WebDriverWait(self.driver, 30)
        men_menu = wait.until(ec.element_to_be_clickable((By.XPATH, path)))
        ActionChains(self.driver).move_to_element(men_menu).perform()



