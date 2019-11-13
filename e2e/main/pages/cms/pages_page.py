import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage

class PagesPage():

    PATH_PAGES_BUTTON = "//a[contains(text(), 'Pages')]"
    PATH_EDIT_BUTTON = "//span[contains(text(), 'Edit')]"
    PATH_DELETE_BUTTON = "//span[@class='icon fa fa-trash-o']"
    PATH_OK_BUTTON = "//button[contains(text(), 'OK')]"
    PATH_ADD_PAGE_BUTTON = "//span[@class='icon fa fa-plus']"

    PATH_PAGES_BODY_FIELD = "//p[contains(text(), 'Add the content you want students to see on this page.')]"
    PATH_SETTINGS_BUTTON = "//a[@class='settings-button']"
    PATH_PAGES_NAME_BUTTON = "//input[@class='input setting-input']"
    PATH_SAVE_BUTTON = "//a[contains(text(), 'Save')]"
    PATH_PAGES_TEXT = "//section[@class='container']"
    PATH_PAGES_LIST = "//div[@class='tab-list']"


    def __init__(self, driver, *args, **kwargs):
        super(PagesPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)

    def open_pages(self):
        '''Open Pages'''
        self.logger.do_click('Settings')
        self.driver.find_element_by_xpath(self.course_outline_page.PATH_CONTENT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Pages')
        self.driver.find_element_by_xpath(self.PATH_PAGES_BUTTON).click()
        time.sleep(3)

    def open_new_page(self, pagesName):
        '''Open Progress'''
        self.logger.do_click('New page')
        self.driver.find_element_by_xpath("//a[contains(text(), '" + pagesName + "')]").click()
        time.sleep(3)

    def add_page(self):
        '''Add Page'''
        self.logger.do_click('Add a New Page')
        self.driver.find_element_by_xpath(self.PATH_ADD_PAGE_BUTTON).click()
        time.sleep(3)

    def delete_page(self):
        '''Delete Page'''
        self.logger.do_click('Delete Page')
        self.driver.find_element_by_xpath(self.PATH_DELETE_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('OK')
        self.driver.find_element_by_xpath(self.PATH_OK_BUTTON).click()
        time.sleep(3)

    def change_page(self, name):
        '''Add Page'''
        self.logger.do_click('EDIT')
        self.driver.find_element_by_xpath(self.PATH_EDIT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('SETTINGS')
        self.config.execute_script_click(self.PATH_SETTINGS_BUTTON)
        time.sleep(1)
        self.logger.do_input('Pages name = "' + name + '"')
        self.driver.find_element_by_xpath(self.PATH_PAGES_NAME_BUTTON).clear()
        self.driver.find_element_by_xpath(self.PATH_PAGES_NAME_BUTTON).send_keys(name)
        self.logger.do_click('Save')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(3)

    def set_page_unvisible(self, page):
        '''Set page visible/unvisible'''
        self.logger.do_click('Set page visible/unvisible')
        self.driver.find_element_by_xpath("//li[@data-tab-id='" + page.lower()  + "']/div[2]").click()
        time.sleep(3)

    def change_pages_plase(self, firstPage, secondPage):
        '''change pages plase'''
        source_element = self.driver.find_element_by_xpath("//li[@data-tab-id='" + firstPage.lower() + "']/div[3]")
        dest_element = self.driver.find_element_by_xpath("//li[@data-tab-id='" + secondPage.lower() + "']/div[3]")
        ActionChains(self.driver).drag_and_drop(source_element, dest_element).perform()
        time.sleep(3)




    def get_possible_edit_page(self):
        '''Get possible edit page in CMS'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_EDIT_BUTTON).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_possible_delete_page(self):
        '''Get possible delete page in CMS'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_DELETE_BUTTON).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_pages_text(self):
        '''Get pages text in LMS on pages page'''
        return self.driver.find_element_by_xpath(self.PATH_PAGES_TEXT).text.replace('\n', '; ')

    def get_pages_list(self):
        '''Get pages text in CMS'''
        return self.driver.find_element_by_xpath(self.PATH_PAGES_LIST).text.replace('\n', '; ')

    def get_pages_location(self, page):
        '''Get pages location'''
        return self.driver.find_element_by_xpath("//li[@data-tab-id='" + page.lower() + "']/div[3] | "
                                                "//a[contains(text(), '" + page + "')]").location