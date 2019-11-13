import time
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables

class DiscussionPage():

    PATH_DISCUSSION_BUTTON = "//a[contains(@href, 'forum')]"
    PATH_ADD_POST_BUTTON = "//button[@class='btn btn-outline-primary btn-small new-post-btn'] | //button[@class='btn btn-small new-post-btn'] | " \
                           "//button[@class='btn-link new-post-btn']"
    PATH_SHOW_DISCUSSION_BUTTON = "//span[contains(text(), 'Show Discussion')]"
    PATH_CREATE_QUESTION_BUTTON = "//div[@class='field-label']/label[1] | //fieldset[@class='field-input']/label[1]"
    PATH_CREATE_DISCUSSION_BUTTON = "//div[@class='field-label']/label[2] | //fieldset[@class='field-input']/label[2]"
    PATH_TITLE_FIELD = "//input[@class='js-post-title field-input'] | //input[@class='edit-post-title field-input']"
    PATH_TITLE_CHANGE_FIELD = "//input[@class='edit-post-title field-input']"
    PATH_TITLE = "//div[@class='post-header-content']/h2 | //div[@class='post-header-content']/h4"
    PATH_IDEA_FIELD = "//textarea[@id='wmd-input-js-post-body-undefined'] | //textarea[@id='wmd-input-edit-post-body-undefined']"
    PATH_IDEA_CHANGE_FIELD = "//textarea[@id='wmd-input-edit-post-body-undefined']"
    PATH_IDEA = "//div[@class='post-body']"
    PATH_REPLY_FIELD = "//div[@class='wmd-panel']/textarea"
    PATH_DISCUSSION_ALL_TEXT = "//main[@class='discussion-column'] | //div[@class='forum-content']"
    PATH_SUBMIT_BUTTON = "//button[@class='btn btn-primary submit'] | //button[@class='btn-brand submit']"
    PATH_SUBMIT_CHANGE_BUTTON = "//button[@class='btn btn-outline-primary discussion-submit-post control-button'] | //button[@class='btn discussion-submit-post control-button']"
    PATH_UPDATE_POST_BUTTON = "//button[@id='edit-post-submit']"

    PATH_ALL_DISCUSSION_BUTTON = "//span[contains(text(), 'All Discussions')]"
    PATH_FIRST_POST_BUTTON = "//div[@class='thread-preview-body']"

    PATH_MORE_BUTTON = "//span[@class='icon fa fa-ellipsis-h']"
    PATH_MORE_PIN_BUTTON = "//button[@class='btn-link action-list-item action-pin']"
    PATH_MORE_UNPIN_BUTTON = "//button[@class='btn-link action-list-item action-pin is-checked']"
    PATH_MORE_EDIT_BUTTON = "//button[@class='btn-link action-list-item action-edit']"
    PATH_MORE_DELETE_BUTTON = "//button[@class='btn-link action-list-item action-delete']"
    PATH_MORE_REPORT_BUTTON = "//button[@class='btn-link action-list-item action-report']"
    PATH_MORE_UNREPORT_BUTTON = "//button[@class='btn-link action-list-item action-report is-checked']"
    PATH_MORE_CLOSE_BUTTON = "//button[@class='btn-link action-list-item action-close']"
    PATH_MORE_OPEN_BUTTON = "//button[@class='btn-link action-list-item action-close is-checked']"

    PATH_LABELS = "//div[@class='post-header-content']/div"
    PATH_PREVIEW = "//span[contains(text(), 'Preview')]"
    PATH_DISCUSSION_ID = "//li[@class='forum-nav-thread']"

    def __init__(self, driver, *args, **kwargs):
        super(DiscussionPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_discussion(self):
        '''Open discussion'''
        self.logger.do_click('Discussion')
        self.driver.find_element_by_xpath(self.PATH_DISCUSSION_BUTTON).click()
        time.sleep(3)

    def input_title(self, title, activity):
        '''Input title'''
        self.logger.do_input('Title = "' + title + '"')
        if(activity == variables.STATUS_INPUT):
            self.driver.find_element_by_xpath(self.PATH_TITLE_FIELD).send_keys(title)
        elif(activity == variables.STATUS_CHANGE):
            self.driver.find_element_by_xpath(self.PATH_TITLE_CHANGE_FIELD).clear()
            self.driver.find_element_by_xpath(self.PATH_TITLE_CHANGE_FIELD).send_keys(title)

    def input_idea(self, idea, activity):
        '''Input idea'''
        self.logger.do_input('Idea = "' + idea + '"')
        if (activity == variables.STATUS_INPUT):
            self.driver.find_element_by_xpath(self.PATH_IDEA_FIELD).send_keys(idea)
        elif (activity == variables.STATUS_CHANGE):
            self.driver.find_element_by_xpath(self.PATH_IDEA_CHANGE_FIELD).clear()
            self.driver.find_element_by_xpath(self.PATH_IDEA_CHANGE_FIELD).send_keys(idea)

    def input_reply(self, text):
        '''Input reply'''
        '''Doesn't use now'''
        self.logger.do_click('Reply "' + text + '"')
        #self.config.executeScriptClick(self.PATH_REPLY_FIELD)
        #self.config.executeScriptClick(self.PATH_REPLY_FIELD)
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_SUBMIT_CHANGE_BUTTON).click()
        self.driver.find_element_by_xpath(self.PATH_TITLE).click()
        self.config.execute_script_click("//div[@class='wmd-panel']/div/div/button[1]/span")
        self.driver.find_element_by_xpath(self.PATH_REPLY_FIELD).click()
        self.driver.find_element_by_xpath(self.PATH_REPLY_FIELD).send_keys(text)
        time.sleep(1)
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_SUBMIT_CHANGE_BUTTON).click()
        time.sleep(3)

    def save_changes(self):
        '''Save changes'''
        self.logger.do_click('Update post')
        self.driver.find_element_by_xpath(self.PATH_UPDATE_POST_BUTTON).click()
        time.sleep(3)

    def click_show_discussions(self):
        '''Click show discussions'''
        try:
            self.logger.do_click('Show discussions')
            self.driver.find_element_by_xpath(self.PATH_SHOW_DISCUSSION_BUTTON).click()
        except:
            pass

    def create_post(self, type, title, idea):
        '''Create post'''
        self.logger.do_click('Add a post')
        self.driver.find_element_by_xpath(self.PATH_ADD_POST_BUTTON).click()
        time.sleep(1)
        if(type == variables.STATUS_QUESTION):
            self.logger.do_click('Question')
            self.driver.find_element_by_xpath(self.PATH_CREATE_QUESTION_BUTTON).click()
        elif(type == variables.STATUS_DISCUSSION):
            self.logger.do_click('Discussion')
            self.driver.find_element_by_xpath(self.PATH_CREATE_DISCUSSION_BUTTON).click()
        self.input_title(title, variables.STATUS_INPUT)
        self.input_idea(idea, variables.STATUS_INPUT)
        time.sleep(1)
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_SUBMIT_BUTTON).click()
        time.sleep(1)

    def delete_all_posts(self):
        '''Delete all posts'''
        try:
            for i in range(1, 100):
                self.driver.find_element_by_xpath(self.PATH_FIRST_POST_BUTTON).click()
                self.click_delete_discussion()
        except:
            pass

    def open_all_discussion(self):
        '''Open all discussion'''
        self.logger.do_click('All discussion')
        self.driver.find_element_by_xpath(self.PATH_ALL_DISCUSSION_BUTTON).click()
        time.sleep(3)

    def open_some_discussion(self, name):
        '''Open some discussion by name'''
        self.logger.do_click('Discussion "' + name + '"')
        self.driver.find_element_by_xpath("//span[contains(text(), '" + name + "')]").click()
        time.sleep(1)

    def click_pin_discussion(self):
        '''Click pin discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Pin')
        self.driver.find_element_by_xpath(self.PATH_MORE_PIN_BUTTON).click()
        time.sleep(1)

    def click_unpin_discussion(self):
        '''Click unpin discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Unpin')
        self.driver.find_element_by_xpath(self.PATH_MORE_UNPIN_BUTTON).click()
        time.sleep(1)

    def click_edit_discussion(self):
        '''Click edit discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Edit')
        self.driver.find_element_by_xpath(self.PATH_MORE_EDIT_BUTTON).click()
        time.sleep(1)

    def click_delete_discussion(self):
        '''Click delete discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Delete')
        self.driver.find_element_by_xpath(self.PATH_MORE_DELETE_BUTTON).click()
        time.sleep(1)
        self.driver.switch_to_alert().accept()

    def click_report_discussion(self):
        '''Click report discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Report')
        self.driver.find_element_by_xpath(self.PATH_MORE_REPORT_BUTTON).click()
        time.sleep(1)

    def click_unreport_discussion(self):
        '''Click unreport discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Unreport')
        self.driver.find_element_by_xpath(self.PATH_MORE_UNREPORT_BUTTON).click()
        time.sleep(1)

    def click_close_discussion(self):
        '''Click close discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Close')
        self.driver.find_element_by_xpath(self.PATH_MORE_CLOSE_BUTTON).click()
        time.sleep(1)

    def click_open_discussion(self):
        '''Click open discussion'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        self.logger.do_click('Open')
        self.driver.find_element_by_xpath(self.PATH_MORE_OPEN_BUTTON).click()
        time.sleep(3)



    def get_present_button_submit(self):
        '''Get present button submit'''
        result = "1"
        try:
            assert (self.driver.find_element_by_xpath(self.PATH_SUBMIT_CHANGE_BUTTON).is_displayed())
        except:
            result = "0"
        return result

    def get_labels(self):
        '''Get labels'''
        return self.driver.find_element_by_xpath(self.PATH_LABELS).text.replace('\n', '; ')

    def get_discussion_all_text(self):
        '''Get Reply'''
        return self.driver.find_element_by_xpath(self.PATH_DISCUSSION_ALL_TEXT).text.replace('\n', '; ')

    def get_discussion_id(self):
        '''Get discussion id'''
        return self.driver.find_element_by_xpath(self.PATH_DISCUSSION_ID).get_attribute("data-id")

    def get_possible_change_post(self):
        '''Click possible change post'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        result = "1"
        try:
            assert (self.driver.find_element_by_xpath(self.PATH_MORE_EDIT_BUTTON).is_displayed())
        except:
            result = "0"
        return result

    def get_possible_delete_post(self):
        '''Click possible delete post'''
        self.logger.do_click('More')
        self.driver.find_element_by_xpath(self.PATH_MORE_BUTTON).click()
        result = "1"
        try:
            assert (self.driver.find_element_by_xpath(self.PATH_MORE_DELETE_BUTTON).is_displayed())
        except:
            result = "0"
        return result

    def get_deleted_post(self, name):
        '''Click possible change post'''
        result = "1"
        try:
            self.driver.find_element_by_xpath("//span[contains(text(), '" + name + "')]").click()
        except:
            result = "0"
        return result



