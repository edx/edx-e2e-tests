import unittest
from selenium import webdriver
from e2e.main.conf import variables

class MainClass(unittest.TestCase):

    def setUp(self):
        '''Open driver, input url and make page fool screen'''
        self.driver = webdriver.Chrome(variables.PATH_TO_LIB + '/chromedriver_77.exe')
        self.driver.maximize_window()

    def tearDown(self):
        '''Close driver'''
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()