import time
from e2e.main.conf import variables
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from selenium.common.exceptions import NoSuchElementException

class CoursePage():
    PATH_SEARCH_FIELD = "//input[@id='search'] | //input[@id='course-search-input']"
    PATH_SEARCH_BUTTON = "//button[contains(text(), 'Search')]"
    PATH_VIEW_BUTTON = "//a[@class='result-link']"

    PATH_COURSE_BUTTON = "//a[contains(@href, '/courseware')] | //a[contains(@href, '/course/')]"
    PATH_SECTION_BUTTON = "//span[@class='group-heading']/span"
    PATH_SUBSECTION_BUTTON = "//div[@class='subsection-text'] | //p[@class='accordion-display-name']"
    PATH_UNIT_BUTTON = "//div[@class='vertical-title'] | //span[@class='icon fa seq_problem'] | //span[@class='subsection-title'] | //span[@class='icon fa seq_other']"
    PATH_CHOISE_BUTTON_SECOND = "//input[contains(@id, '_choice_1')]"
    PATH_CHOISE_BUTTON_FIRST = "//input[contains(@id, '_choice_0')]"
    PATH_SUBMIT_BUTTON = "//span[contains(text(), 'Submit')]"
    PATH_VISIBLE_SUBMIT_BUTTON = "//button[@class='submit btn-brand']"
    PATH_UNIT_LIST = "//nav[@class='course-navigation'] | //ol[@class='block-tree accordion'] | //div[@class='page-content']"
    PATH_UPPER_UNIT_LIST = "//section[@class='course-content'] | //div[@class='course-view page-content-container'] | //div[@class='course-view container'] | //div[@class='course-wrapper']"
    PATH_VISIBLE_RESULT = "//span[@class='status submitted'] | //span[@class='status correct'] | //span[@class='status incorrect']"
    PATH_ALL_COURSE_INFORMATION = "//ul[@class='navbar-nav mr-auto'] | //ol[@class='tabs course-tabs']"

    PATH_SHOW_ANSWER_BUTTON = "//button[@class='show problem-action-btn btn-default btn-small']"
    PATH_SHOW_ANSWER_CHECK_CLASS = "//input[contains(@id, '_choice_1')]/parent::label"
    PATH_CALCULATOR_BUTTON = "//span[@class='icon fa fa-calculator']"
    PATH_CALCULATOR_INPUT_FIELD = "//input[@id='calculator_input']"
    PATH_CALCULATOR_GET_RESULT_BUTTON = "//input[@id='calculator_button']"
    PATH_CALCULATOR_RESULT_FIELD = "//input[@id='calculator_output']"
    PATH_RESET_BUTTON = "//button[@class='reset problem-action-btn btn-default btn-small']"
    PATH_LICENSES = "//div[@class='course-license']"
    PATH_COURSE_CONTENT = "//div[@class='page-content'] | //div[@class='container']"
    PATH_UPDATES_BUTTON = "//a[@data-analytics-id='edx.updates'] | //button[contains(text(), 'Show')]"

    PATH_NEXT_BUTTON = "//span[contains(text(), 'Next')]"
    #ORA
    PATH_SAVE_YOUR_PROGRESS_BUTTON = "//button[@class='action action--save submission__save']"
    PATH_ORA_TEXT_FIELD = "//textarea[@class='submission__answer__part__text__value']"
    PATH_ORA_FIRST_SUBMIT_BUTTON = "//button[@class='action action--submit step--response__submit']"
    PATH_ORA_SECOND_SUBMIT_BUTTON = "//button[@class='student-training--001__assessment__submit action action--submit']"
    PATH_ORA_THIRD_SUBMIT_BUTTON = "//button[@class='peer-assessment--001__assessment__submit action action--submit']"
    PATH_ORA_FOURTH_SUBMIT_BUTTON = "//button[@class='self-assessment--001__assessment__submit action action--submit']"
    PATH_ORA_FIFTH_SUBMIT_BUTTON = "//button[@class='action action--submit continue_grading--action']"
    PATH_ORA_MANAGE_LEARNERS_BUTTON = "//button[contains(text(), 'Manage Individual Learners')]"
    PATH_ORA_GRADE_AVAILABLE_BUTTON = "//button[contains(text(), 'Grade Available Responses')]"
    PATH_STAFF_ASSESSMENT_BUTTON = "//button[contains(text(), 'Staff Assessment')]"

    PATH_ORA_LEARNERS_EMAIL_FIELD = "//input[@class='openassessment__student_username value']"

    PATH_STAFF_DENUG_INFO_BUTTON = "//a[contains(text(), 'Staff Debug Info')]"
    PATH_STAFF_ACTIONS_FIELD = "//div[@class='staff_actions']/div/input"
    PATH_STAFF_DEBUG_DELETE_BUTTON = "//button[@class='btn-link staff-debug-sdelete']"



    def __init__(self, driver, *args, **kwargs):
        super(CoursePage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)

    def open_course(self):
        '''Open Course'''
        self.logger.do_click('Course')
        self.config.wait_element(self.PATH_COURSE_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_COURSE_BUTTON).click()
        time.sleep(3)

    def search_course(self, text):
        '''Search some info on course'''
        self.logger.do_input('Search by = "' + text + '"')
        self.driver.find_element_by_xpath(self.PATH_SEARCH_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_SEARCH_FIELD).send_keys(text)
        time.sleep(1)
        self.logger.do_click('Search')
        self.driver.find_element_by_xpath(self.PATH_SEARCH_BUTTON).click()
        time.sleep(3)

    def click_view(self):
        '''Click View'''
        self.logger.do_click('View')
        self.driver.find_element_by_xpath(self.PATH_VIEW_BUTTON).click()
        time.sleep(3)

    def click_next(self):
        '''Click next'''
        try:
            self.logger.do_click('Next')
            self.driver.find_element_by_xpath(self.PATH_NEXT_BUTTON).click()
            time.sleep(3)
        except:
            pass

    def select_unit(self, unit):
        '''Select unit'''
        self.logger.do_click('Select ' + str(unit) + ' unit')
        self.driver.find_element_by_xpath("//nav[@class='sequence-list-wrapper']/ol/li[" + str(unit) + "]").click()
        time.sleep(3)

    def open_unit(self):
        '''Open unit'''
        self.logger.do_click('Unit')
        self.driver.find_element_by_xpath(self.PATH_UNIT_BUTTON).click()
        time.sleep(3)

    def open_section(self):
        '''Open unit'''
        self.logger.do_click('Section')
        self.driver.find_element_by_xpath(self.PATH_SECTION_BUTTON).click()
        time.sleep(1)

    def open_subsection(self):
        '''Open unit'''
        self.logger.do_click('Subsection')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_BUTTON).click()
        time.sleep(1)

    def open_updates(self):
        '''Open unit'''
        self.logger.do_click('Updates')
        self.driver.find_element_by_xpath(self.PATH_UPDATES_BUTTON).click()
        time.sleep(1)

    def correct_answer_unit(self, unit):
        '''Answer unit'''
        self.logger.do_click('Unit')
        self.driver.find_element_by_xpath(self.PATH_UNIT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Select ' + str(unit) + ' unit')
        self.driver.find_element_by_xpath("//nav[@class='sequence-list-wrapper']/ol/li[" + str(unit) +"]").click()
        time.sleep(1)
        self.logger.do_click('Correct answer')
        self.driver.find_element_by_xpath(self.PATH_CHOISE_BUTTON_SECOND).click()
        time.sleep(1)
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_SUBMIT_BUTTON).click()
        time.sleep(5)

    def incorrect_answer_unit(self, unit):
        '''Answer unit'''
        self.logger.do_click('Unit')
        self.driver.find_element_by_xpath(self.PATH_UNIT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Unit')
        self.driver.find_element_by_xpath("//div[@class='vertical-title'] | //nav[@class='sequence-list-wrapper']/ol/li[" + str(unit) + "]").click()
        time.sleep(1)
        self.logger.do_click('Incorrect answer')
        self.driver.find_element_by_xpath(self.PATH_CHOISE_BUTTON_FIRST).click()
        time.sleep(1)
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_SUBMIT_BUTTON).click()
        time.sleep(5)

    def input_ora_first_block(self, text):
        '''Input first block ORA'''
        self.logger.do_input('Text = "' + text + '"')
        self.driver.find_element_by_xpath(self.PATH_ORA_TEXT_FIELD).send_keys(text)

    def click_save_ora_first_block(self):
        '''Click Save first block ORA'''
        self.logger.do_click('Save your progress')
        self.driver.find_element_by_xpath(self.PATH_SAVE_YOUR_PROGRESS_BUTTON).click()
        time.sleep(1)

    def complete_ora_first_block(self, text):
        '''Complete first block ORA'''
        self.input_ora_first_block(text)
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_ORA_FIRST_SUBMIT_BUTTON).click()
        time.sleep(1)
        self.driver.switch_to_alert().accept()
        time.sleep(5)

    def complete_ora_second_block(self, firstUnswer, secondUnswer, thirdUnswer, fourthUnswer):
        '''Complete second block ORA'''
        self.config.do_assert_true_in(variables.TEXT_IN_PROGRESS_1, self.get_about_unit_text())
        self.logger.do_click('Unswer № ' + str(firstUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[1]/div[2]/div[3]/div[" + str(firstUnswer) + "]/div[1]/input | "
                                          "//div[@class='assessment__fields']/ol/li[1]/div[2]/div[3]/div/div[" + str(firstUnswer) + "]/div[1]/input").click()
        self.logger.do_click('Unswer № ' + str(secondUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[2]/div[2]/div[3]/div[" + str(secondUnswer) + "]/div[1]/input | "
                                          "//div[@class='assessment__fields']/ol/li[2]/div[2]/div[3]/div/div[" + str(secondUnswer) + "]/div[1]/input").click()
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_ORA_SECOND_SUBMIT_BUTTON).click()
        time.sleep(5)
        self.config.do_assert_true_in(variables.TEXT_IN_PROGRESS_2, self.get_about_unit_text())
        self.logger.do_click('Unswer №' + str(thirdUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[1]/div[2]/div[3]/div[" + str(thirdUnswer) + "]/div/input | "
                                          "//div[@class='assessment__fields']/ol/li[1]/div[2]/div[3]/div/div[" + str(thirdUnswer) + "]/div[1]/input").click()
        self.logger.do_click('Unswer № ' + str(fourthUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[2]/div[2]/div[3]/div[" + str(fourthUnswer) + "]/div/input | "
                                          "//div[@class='assessment__fields']/ol/li[2]/div[2]/div[3]/div/div[" + str(fourthUnswer) + "]/div[1]/input").click()
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_ORA_SECOND_SUBMIT_BUTTON).click()
        time.sleep(5)

    def complete_ora_third_block(self, firstUnswer, secondUnswer):
        '''Complete second block ORA'''
        result = "1"
        try:
            self.logger.do_click('Unswer № ' + str(firstUnswer))
            self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[1]/div[2]/div/div/div[" + str(firstUnswer) + "]/div/input").click()
            self.logger.do_click('Unswer № ' + str(secondUnswer))
            self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[2]/div[2]/div/div/div[" + str(secondUnswer) + "]/div/input").click()
            self.logger.do_click('Submit')
            self.driver.find_element_by_xpath(self.PATH_ORA_THIRD_SUBMIT_BUTTON).click()
            time.sleep(5)
        except:
            result = "0"
        return result

    def complete_ora_fourth_block(self, firstUnswer, secondUnswer):
        '''Complete second block ORA'''
        self.logger.do_click('Unswer № ' + str(firstUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[1]/div[2]/div/div/div[" + str(firstUnswer) + "]/div/input").click()
        self.logger.do_click('Unswer № ' + str(secondUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[2]/div[2]/div/div/div[" + str(secondUnswer) + "]/div/input").click()
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_ORA_FOURTH_SUBMIT_BUTTON).click()
        time.sleep(5)

    def complete_ora_fifth_block(self, firstUnswer, secondUnswer):
        '''Complete second block ORA'''
        self.logger.do_click('Unswer № ' + str(firstUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[1]/div[2]/div/div/div[" + str(firstUnswer) + "]/div/input").click()
        self.logger.do_click('Unswer № ' + str(secondUnswer))
        self.driver.find_element_by_xpath("//div[@class='assessment__fields']/ol/li[2]/div[2]/div/div/div[" + str(secondUnswer) + "]/div/input").click()
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_ORA_FIFTH_SUBMIT_BUTTON).click()
        time.sleep(5)

    def click_manage_individual_learners(self):
        '''Click manage individual learners'''
        self.logger.do_click('Manage individual learners')
        self.driver.find_element_by_xpath(self.PATH_ORA_MANAGE_LEARNERS_BUTTON).click()
        time.sleep(1)

    def click_grade_available_responses(self):
        '''Click grade available responses'''
        self.logger.do_click('Grade available responses')
        self.driver.find_element_by_xpath(self.PATH_ORA_GRADE_AVAILABLE_BUTTON).click()
        time.sleep(1)

    def click_staff_assessment(self):
        '''Click staff assessment'''
        self.logger.do_click('Staff assessment')
        self.driver.find_element_by_xpath(self.PATH_STAFF_ASSESSMENT_BUTTON).click()
        time.sleep(1)

    def input_learners_email(self, email):
        '''Input learners email/name'''
        self.logger.do_input('Email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_ORA_LEARNERS_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ORA_LEARNERS_EMAIL_FIELD).send_keys(email)
        self.logger.do_click('Submit')
        self.driver.find_element_by_xpath(self.PATH_SUBMIT_BUTTON).click()
        time.sleep(1)

    def click_ora_staff_viewing(self, button):
        '''Click ora staff viewing'''
        self.logger.do_click(button)
        self.driver.find_element_by_xpath("//button[contains(@id, '" + button + "')]").click()
        time.sleep(3)

    def delete_user_answer(self, name):
        '''Delete user answer'''
        self.driver.find_element_by_xpath(self.PATH_STAFF_DENUG_INFO_BUTTON).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(self.PATH_STAFF_ACTIONS_FIELD).send_keys(name)
        self.driver.find_element_by_xpath(self.PATH_STAFF_DEBUG_DELETE_BUTTON).click()
        time.sleep(1)
        self.config.refresh_page()

    def click_show_answer(self):
        '''Click show answer'''
        self.logger.do_click('Show answer')
        self.driver.find_element_by_xpath(self.PATH_SHOW_ANSWER_BUTTON).click()
        time.sleep(1)

    def click_reset(self):
        '''Click show answer'''
        self.logger.do_click('Reset')
        self.driver.find_element_by_xpath(self.PATH_RESET_BUTTON).click()
        time.sleep(1)

    def click_calculator(self):
        '''Click calculator'''
        self.logger.do_click('Calculator')
        self.driver.find_element_by_xpath(self.PATH_CALCULATOR_BUTTON).click()
        time.sleep(1)

    def input_calculator_value(self, value):
        '''Input calculator value'''
        self.logger.do_input('Value = "' + value + '"')
        self.driver.find_element_by_xpath(self.PATH_CALCULATOR_INPUT_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_CALCULATOR_INPUT_FIELD).send_keys(value)
        self.driver.find_element_by_xpath(self.PATH_CALCULATOR_GET_RESULT_BUTTON).click()
        time.sleep(1)



    def get_unit_list_text(self):
        '''Get unit list'''
        return self.driver.find_element_by_xpath(self.PATH_UNIT_LIST).text.replace('\n', '; ')

    def get_about_unit_text(self):
        '''Get unit list'''
        return self.driver.find_element_by_xpath(self.PATH_UPPER_UNIT_LIST).text.replace('\n', '; ')

    def get_ora_text(self):
        '''Get unit list'''
        return self.driver.find_element_by_xpath("//textarea[@class='submission__answer__part__text__value']").get_attribute("value")

    def get_activity_submit(self):
        '''Get visible submit button'''
        return self.driver.find_element_by_xpath(self.PATH_VISIBLE_SUBMIT_BUTTON).get_attribute("data-should-enable-submit-button").lower()

    def get_visible_result(self):
        '''Get visible result'''
        return self.driver.find_element_by_xpath(self.PATH_VISIBLE_RESULT).get_attribute("data-tooltip")

    def get_all_course_information_text(self):
        '''Get all course information'''
        return self.driver.find_element_by_xpath(self.PATH_ALL_COURSE_INFORMATION).text.replace('\n', '; ')

    def get_visible_correct_result(self):
        '''Get visible message correct result'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_VISIBLE_RESULT).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_visible_show_answer(self):
        '''Get visible show answer'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_SHOW_ANSWER_BUTTON).is_enabled()
        except NoSuchElementException:
            result = "0"
        return result

    def get_clicable_submit_ora_first_block(self):
        '''Get clicable submit ora first block'''
        result = "1"
        try:
            self.driver.find_element_by_xpath(self.PATH_ORA_FIRST_SUBMIT_BUTTON).click()
        except:
            result = "0"
        return result

    def get_calculator_result(self):
        '''Get calculator result'''
        return self.driver.find_element_by_xpath(self.PATH_CALCULATOR_RESULT_FIELD).get_attribute('value')

    def get_show_answer_class(self):
        '''Get show answer class'''
        return self.driver.find_element_by_xpath(self.PATH_SHOW_ANSWER_CHECK_CLASS).get_attribute('class')

    def get_licenses_text(self):
        '''Get licenses text'''
        return self.driver.find_element_by_xpath(self.PATH_LICENSES).text.replace('\n', '; ')

    def get_course_content_text(self):
        '''Get licenses text'''
        return self.driver.find_element_by_xpath(self.PATH_COURSE_CONTENT).text.lower()