import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables
from e2e.main.conf.config import Config

class CourseOutlinePage():
    PATH_OUTLINE_BUTTON = "//a[contains(text(), 'Outline')]"
    PATH_COURSE_OUTLINE = "//h1[@class='page-header']"
    PATH_TEST_COURSE = "//a[@href='/course/" + variables.ID_BASE_COURSE + "']"
    PATH_XBLOCK_EDITOR = "//div[@class='xblock-editor']"
    PATH_ARCHIVED_COURSES_BUTTON = "//li[@class='archived-courses-tab']"

    PATH_CONTENT_BUTTON = "//span[contains(text(), 'Content')]"
    PATH_SETTINGS_BUTTON = "//span[contains(text(), 'Settings')] | //span[contains(text(), 'Настройки')]"
    PATH_TOOLS_BUTTON = "//span[contains(text(), 'Tools')]"

    PATH_NEW_COURSE_BUTTON = "//a[@class='button new-button new-course-button']"
    PATH_COURSE_NAME_FIELD = "//input[@id='new-course-name']"
    PATH_ORGANIZATION_FIELD = "//input[@id='new-course-org']"
    PATH_COURSE_NUMBER_FIELD = "//input[@id='new-course-number']"
    PATH_COURSE_RUN_FIELD = "//input[@id='new-course-run']"
    PATH_CREATE_BUTTON = "//input[@type='submit']"
    PATH_REINDEX_BUTTON = "//a[@title='Reindex current course']"
    PATH_SAVE_BUTTON = "//a[contains(text(), 'Save')]"
    PATH_CANCEL_BUTTON = "//a[contains(text(), 'Cancel')]"

    PATH_NEW_SECTION_BUTTON = "//a[@class='button button-new']"
    PATH_VISIBILITY_BUTTON = "//button[contains(text(), 'Visibility')] | //button[contains(text(), 'Advanced')]"
    PATH_SECTION_BUTTON = "//a[@class='navigation-item navigation-link navigation-parent']"
    PATH_SECTION_CONFIGURE = "//div[@class='section-header-actions']/ul/li[@class='action-item action-configure']"
    PATH_SECTION_NAME_FIELD = "//input[@value='Section']"
    PATH_SECTION_START_FIELD = "//input[@id='start_date']"
    PATH_COURSES_GROUPS_TEXT = "//p[@class='status-message-copy']"

    PATH_NEW_SUBSECTION_BUTTON = "//a[@title='Click to add a new Subsection']"
    PATH_SUBSECTION_BUTTON = "//span[@class='subsection-title item-title xblock-field-value incontext-editor-value']"
    PATH_SUBSECTION_CONFIGURE = "//div[@class='subsection-header-actions']/ul/li[@class='action-item action-configure']"
    PATH_SUBSECTION_NAME_FIELD = "//input[@value='Subsection']"
    PATH_SUBSECTION_START_FIELD = "//input[@id='start_date']"
    PATH_SUBSECTION_END_FIELD = "//input[@id='due_date']"
    PATH_HIDE_AFTER_DUE_BUTTON = "//input[@value='hide_after_due']"
    PATH_STAFF_ONLY_BUTTON = "//input[@value='staff_only']"
    PATH_NEVER_BUTTON = "//input[@value='never']"
    PATH_PAST_DUE_BUTTON = "//input[@value='past_due']"

    PATH_NEW_UNIT_BUTTON = "//a[@title='Click to add a new Unit']"
    PATH_UNIT_BUTTON = "//a[contains(text(), 'Unit')]"
    PATH_EDIT_BUTTON = "//ul[@class='actions-list']/li/button | //ul[@class='actions-list']/li/a"
    PATH_XBLOCK_TEXT_FIELD = "//div[@class='CodeMirror-code']"
    PATH_UNIT_SETTINGS_BUTTON = "//a[@class='settings-button'] | //a[@class='ui-tabs-anchor']"
    PATH_ADVANCED_BUTTON = "//li[@class='ui-state-default ui-corner-top']"
    PATH_PROBLEM_BUTTON = "//span[@class='large-template-icon large-problem-icon']"
    PATH_DISCUSSION_BUTTON = "//span[@class='large-template-icon large-discussion-icon']"
    PATH_MULTIPLE_CHOISE_BUTTON = "//span[contains(text(), 'Multiple Choice')]"
    PATH_PUBLISH_BUTTON = "//span[@class='icon fa fa-upload'] | //a[@class='action-publish action-primary ']"
    PATH_PUBLISH_CONFIRM_BUTTON = "//a[contains(text(), 'Publish')]"
    PATH_UNIT_CONFIGURE = "//div[@class='unit-header-actions']/ul/li[@class='action-item action-configure']"
    PATH_UNIT_NAME_FIELD = "//input[@value='Unit']"
    PATH_GRADING_TYPE_FIELD = "//select[@id='grading_type']"
    PATH_UNIT_VISIBLE = "//input[@id='staff_lock'] | //li[@class='field field-checkbox checkbox-cosmetic']"
    PATH_RESTRICT_ACCESS_FIELD = "//select[@id='partition-select']"
    PATH_CONTENT_GROUP_BUTTON = "//option[contains(text(), 'Content Groups')]"
    PATH_MAXIMUM_ATTEMPTS_FIELD = "//input[@class='input setting-input setting-input-number']"
    PATH_SHOW_ANSWER_FIELD = "//select[@name='Show Answer']"
    PATH_SHOW_RESET_FIELD = "//select[@name='Show Reset Button']"

    PATH_TEXT_RESPONSE_FIELD = "//select[@id='openassessment_submission_text_response']"
    PATH_FILE_UPLOAD_FIELD = "//select[@id='openassessment_submission_file_upload_response']"
    PATH_FILE_UPLOAD_TIPE_FIELD = "//select[@id='openassessment_submission_upload_selector']"
    PATH_FILE_UPLOAD_OTHER_TIPE_FIELD = "//input[@id='openassessment_submission_white_listed_file_types']"
    PATH_MUST_GRADE_FIELD = "//input[@id='peer_assessment_must_grade']"
    PATH_GRADE_BY_FIELD = "//input[@id='peer_assessment_graded_by']"
    PATH_STAFF_ASSESSMENT_BUTTON = "//input[@id='include_staff_assessment']"

    def __init__(self, driver, *args, **kwargs):
        super(CourseOutlinePage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)

    def open_outline(self):
        '''Open Outline'''
        self.logger.do_click('Content')
        self.driver.find_element_by_xpath(self.PATH_CONTENT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Outline')
        self.driver.find_element_by_xpath(self.PATH_OUTLINE_BUTTON).click()
        time.sleep(3)

    def click_save(self):
        '''Click Save'''
        self.logger.do_click('Save')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(5)

    def click_cancel(self):
        '''Click Cancel'''
        self.logger.do_click('Cancel')
        self.driver.find_element_by_xpath(self.PATH_CANCEL_BUTTON).click()
        time.sleep(1)



    def create_course(self, courseName, organization, courseNumber, courseRun):
        '''Create course'''
        self.logger.do_click('New course')
        self.config.wait_element(self.PATH_NEW_COURSE_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_NEW_COURSE_BUTTON).click()
        time.sleep(1)
        self.logger.do_input('Course name = "' + courseName + '"')
        self.config.wait_element(self.PATH_COURSE_NAME_FIELD)
        self.driver.find_element_by_xpath(self.PATH_COURSE_NAME_FIELD).send_keys(courseName)
        self.logger.do_input('Organization = "' + organization + '"')
        self.driver.find_element_by_xpath(self.PATH_ORGANIZATION_FIELD).send_keys(organization)
        self.logger.do_input('Course number = "' + courseNumber + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_NUMBER_FIELD).send_keys(courseNumber)
        self.logger.do_input('Course run = "' + courseRun + '"')
        self.driver.find_element_by_xpath(self.PATH_COURSE_RUN_FIELD).send_keys(courseRun)
        self.logger.do_click('Create')
        self.driver.find_element_by_xpath(self.PATH_CREATE_BUTTON).click()
        time.sleep(5)

    def open_course(self):
        '''Open course'''
        self.logger.do_click('Test course')
        try:
            self.driver.find_element_by_xpath(self.PATH_TEST_COURSE).click()
            time.sleep(3)
        except:
            self.driver.find_element_by_xpath(self.PATH_ARCHIVED_COURSES_BUTTON).click()
            self.driver.find_element_by_xpath(self.PATH_TEST_COURSE).click()
            time.sleep(3)

    def open_created_course(self, organization, courseNumber, courseRun):
        '''Open course'''
        self.logger.do_click('Test course "' + organization + "+" + courseNumber + "+" + courseRun + '"')
        try:
            self.driver.find_element_by_xpath("//a[@href='/course/course-v1:" + organization + "+" + courseNumber + "+" + courseRun + "']").click()
        except:
            self.driver.find_element_by_xpath(self.PATH_ARCHIVED_COURSES_BUTTON).click()
            self.driver.find_element_by_xpath("//a[@href='/course/course-v1:" + organization + "+" + courseNumber + "+" + courseRun + "']").click()
        time.sleep(3)

    def click_archived(self):
        '''Click archived'''
        try:
            self.logger.do_click('Archived')
            self.driver.find_element_by_xpath(self.PATH_ARCHIVED_COURSES_BUTTON).click()
        except:
            pass



    def add_section(self, sectionName):
        '''Add section'''
        self.logger.do_click('New Section')
        self.config.wait_element(self.PATH_NEW_SECTION_BUTTON)
        self.driver.find_element_by_xpath(self.PATH_NEW_SECTION_BUTTON).click()
        time.sleep(3)
        self.logger.do_input('Section name = "' + sectionName + '"')
        self.driver.find_element_by_xpath(self.PATH_SECTION_NAME_FIELD).send_keys(sectionName)
        self.driver.find_element_by_xpath(self.PATH_SECTION_NAME_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)

    def set_section_visible(self):
        '''Set unit visible'''
        self.logger.do_click('Unit configure')
        self.driver.find_element_by_xpath(self.PATH_SECTION_CONFIGURE).click()
        time.sleep(1)
        self.logger.do_click('Visibility')
        self.driver.find_element_by_xpath(self.PATH_VISIBILITY_BUTTON).click()
        time.sleep(1)
        self.driver.find_element_by_xpath(self.PATH_UNIT_VISIBLE).click()
        self.click_save()

    def click_section_confrigure(self):
        '''Click section configure'''
        self.logger.do_click('Section configure')
        self.driver.find_element_by_xpath(self.PATH_SECTION_CONFIGURE).click()
        time.sleep(1)

    def set_date_section(self, dateStart):
        '''Set date of subsection'''
        self.click_section_confrigure()
        self.logger.do_input('Start date = "' + dateStart + '"')
        self.driver.find_element_by_xpath(self.PATH_SECTION_START_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_SECTION_START_FIELD).send_keys(dateStart)
        self.driver.find_element_by_xpath(self.PATH_SECTION_START_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.click_save()



    def add_subsection(self, subsectionName):
        '''Add subsection'''
        self.logger.do_click('New Subsection')
        self.driver.find_element_by_xpath(self.PATH_NEW_SUBSECTION_BUTTON).click()
        time.sleep(3)
        self.logger.do_input('Subsection name = "' + subsectionName + '"')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_NAME_FIELD).send_keys(subsectionName)
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_NAME_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)

    def click_subsection_confrigure(self):
        '''Click subsection configure'''
        self.logger.do_click('Subsection configure')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_CONFIGURE).click()
        time.sleep(1)

    def set_date_subsection(self, dateStart, dateEnd):
        '''Set date of subsection'''
        self.click_subsection_confrigure()
        self.logger.do_input('Start date = "' + dateStart + '"')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_START_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_START_FIELD).send_keys(dateStart)
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_START_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.logger.do_input('End date = "' + dateEnd + '"')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_END_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_END_FIELD).send_keys(dateEnd)
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_END_FIELD).send_keys(Keys.ENTER)
        time.sleep(1)
        self.click_save()

    def set_subsection_visibility(self, block, button):
        '''Set date of subsection'''
        self.click_subsection_confrigure()
        self.logger.do_click('Visibility')
        self.driver.find_element_by_xpath(self.PATH_VISIBILITY_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Set' + str(button) + 'activity')
        if (block == 1 and button == 2):
            self.driver.find_element_by_xpath(self.PATH_HIDE_AFTER_DUE_BUTTON).click()
        elif (block == 1 and button == 3):
            self.driver.find_element_by_xpath(self.PATH_STAFF_ONLY_BUTTON).click()
        elif (block == 2 and button == 2):
            self.driver.find_element_by_xpath(self.PATH_NEVER_BUTTON).click()
        elif (block == 2 and button == 3):
            self.driver.find_element_by_xpath(self.PATH_PAST_DUE_BUTTON).click()
        time.sleep(1)
        self.click_save()



    def add_unit(self, unitName, gradingType, xblock):
        '''Add unit'''
        self.logger.do_click('New Unit')
        self.driver.find_element_by_xpath(self.PATH_NEW_UNIT_BUTTON).click()
        time.sleep(3)
        self.logger.do_input('Unit name = "' + unitName + '"')
        self.driver.find_element_by_xpath(self.PATH_UNIT_NAME_FIELD).send_keys(unitName)
        self.driver.find_element_by_xpath(self.PATH_UNIT_NAME_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)
        if(xblock in variables.BLOCK_DISCUSSION):
            self.logger.do_click('Discussion')
            self.driver.find_element_by_xpath(self.PATH_DISCUSSION_BUTTON).click()
            time.sleep(3)
        else:
            self.logger.do_click('Problem')
            self.driver.find_element_by_xpath(self.PATH_PROBLEM_BUTTON).click()
            time.sleep(3)
            self.logger.do_click('Xblock "' + xblock + '"')
            self.driver.find_element_by_xpath("//span[contains(text(), '" + xblock + "')]").click()
            time.sleep(3)

        self.logger.do_click('Section')
        self.driver.find_element_by_xpath(self.PATH_SECTION_BUTTON).click()
        time.sleep(3)
        self.logger.do_click('Publish')
        self.driver.find_element_by_xpath(self.PATH_PUBLISH_BUTTON).click()
        time.sleep(3)
        self.logger.do_click('Publish')
        self.driver.find_element_by_xpath(self.PATH_PUBLISH_CONFIRM_BUTTON).click()
        time.sleep(3)
        if(gradingType is not variables.EMPTY):
            self.logger.do_click('Configure')
            self.driver.find_element_by_xpath(self.PATH_SUBSECTION_CONFIGURE).click()
            time.sleep(3)
            self.logger.do_input('Grading type = "' + gradingType + '"')
            self.driver.find_element_by_xpath(self.PATH_GRADING_TYPE_FIELD).send_keys(gradingType)
            time.sleep(1)
            self.click_save()

    def add_ora(self, unitName, gradingType, xblock, responseText, responseFile, tipeFiles, mustGrade, gradeBy, staffAssessmebt):
        '''Add unit'''
        self.logger.do_click('New Unit')
        self.driver.find_element_by_xpath(self.PATH_NEW_UNIT_BUTTON).click()
        time.sleep(5)
        self.logger.do_input('Unit name = "' + unitName + '"')
        self.driver.find_element_by_xpath(self.PATH_UNIT_NAME_FIELD).send_keys(unitName)
        self.driver.find_element_by_xpath(self.PATH_UNIT_NAME_FIELD).send_keys(Keys.ENTER)
        time.sleep(3)
        self.logger.do_click('Problem')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_BUTTON).click()
        time.sleep(3)
        self.logger.do_click('Advanced')
        self.driver.find_element_by_xpath(self.PATH_ADVANCED_BUTTON).click()
        time.sleep(3)
        self.logger.do_click('Xblock "' + xblock + '"')
        self.driver.find_element_by_xpath("//span[contains(text(), '" + xblock + "')]").click()
        time.sleep(3)
        self.logger.do_click('EDIT')
        self.driver.find_element_by_xpath(self.PATH_EDIT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('SETTINGS')
        self.driver.find_element_by_xpath(self.PATH_UNIT_SETTINGS_BUTTON).click()
        time.sleep(1)
        if(variables.PROJECT not in (variables.PROJECT_GIJIMA + variables.PROJECT_WARDY + variables.PROJECT_SPECTRUM)):
            self.logger.do_input('Response text = "' + responseText + '"')
            self.driver.find_element_by_xpath(self.PATH_TEXT_RESPONSE_FIELD).send_keys(responseText)
            time.sleep(1)
            self.logger.do_input('Response file = "' + responseFile + '"')
            self.driver.find_element_by_xpath(self.PATH_FILE_UPLOAD_FIELD).send_keys(responseFile)
            time.sleep(1)
        if(responseFile in variables.STATUS_REQUIRED + variables.STATUS_OPTIONAL):
            self.logger.do_input('File Upload Types = "' + tipeFiles + '"')
            self.driver.find_element_by_xpath(self.PATH_FILE_UPLOAD_TIPE_FIELD).send_keys(tipeFiles)
            time.sleep(1)
            if(tipeFiles in variables.STATUS_DOC):
                tipe = "doc"
                self.logger.do_input('File Types = "' + tipe + '"')
                self.config.execute_script_input(self.PATH_FILE_UPLOAD_OTHER_TIPE_FIELD, tipe)
                time.sleep(1)

        self.logger.do_input('Must grade = "' + mustGrade + '"')
        self.driver.find_element_by_xpath(self.PATH_MUST_GRADE_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_MUST_GRADE_FIELD).send_keys(mustGrade)
        time.sleep(1)
        self.logger.do_input('Grade by = "' + gradeBy + '"')
        self.driver.find_element_by_xpath(self.PATH_GRADE_BY_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_GRADE_BY_FIELD).send_keys(gradeBy)
        time.sleep(1)
        if(staffAssessmebt in variables.STATUS_ON):
            self.logger.do_click('Staff assessment')
            self.driver.find_element_by_xpath(self.PATH_STAFF_ASSESSMENT_BUTTON).click()
            time.sleep(1)
        self.click_save()

        result = "1"
        try:
            self.logger.do_click('Section')
            self.driver.find_element_by_xpath(self.PATH_SECTION_BUTTON).click()
            time.sleep(3)
            self.logger.do_click('Publish')
            self.driver.find_element_by_xpath(self.PATH_PUBLISH_BUTTON).click()
            time.sleep(3)
            self.logger.do_click('Publish')
            self.driver.find_element_by_xpath(self.PATH_PUBLISH_CONFIRM_BUTTON).click()
            time.sleep(3)
            if(gradingType is not variables.EMPTY):
                self.logger.do_click('Configure')
                self.driver.find_element_by_xpath(self.PATH_SUBSECTION_CONFIGURE).click()
                time.sleep(3)
                self.logger.do_input('Grading type = "' + gradingType + '"')
                self.driver.find_element_by_xpath(self.PATH_GRADING_TYPE_FIELD).send_keys(gradingType)
                time.sleep(1)
                self.click_save()
        except:
            result = "0"
            return result

    def set_unit_visible(self, status):
        '''Set unit visible'''
        self.logger.do_click('Subsection')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Unit configure')
        self.driver.find_element_by_xpath(self.PATH_UNIT_CONFIGURE).click()
        time.sleep(1)
        if (status == self.get_status_unit_visible()):
            self.driver.find_element_by_xpath(self.PATH_UNIT_VISIBLE).click()
        self.click_save()

    def set_unit_maximum_attempts(self):
        '''Set unit maximum attempts'''
        self.logger.do_click('Subsection')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Unit')
        self.driver.find_element_by_xpath(self.PATH_SAVE_BUTTON).click()
        time.sleep(1)

    def set_content_group(self, group):
        '''Set content group'''
        self.logger.do_click('Subsection')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Unit configure')
        self.driver.find_element_by_xpath(self.PATH_UNIT_CONFIGURE).click()
        time.sleep(1)
        self.logger.do_click('Restrict access')
        self.driver.find_element_by_xpath(self.PATH_RESTRICT_ACCESS_FIELD).click()
        time.sleep(1)
        self.logger.do_click('Content group')
        self.driver.find_element_by_xpath(self.PATH_CONTENT_GROUP_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Group ' + group)
        self.driver.find_element_by_xpath("//label[contains(text(), '" + group + "')]").click()
        time.sleep(1)
        self.click_save()

    def set_unit_settings(self, line, value):
        '''Set content group'''
        self.logger.do_click('Subsection')
        self.driver.find_element_by_xpath(self.PATH_SUBSECTION_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('Unit')
        self.driver.find_element_by_xpath(self.PATH_UNIT_BUTTON).click()
        time.sleep(3)
        self.logger.do_click('EDIT')
        self.driver.find_element_by_xpath(self.PATH_EDIT_BUTTON).click()
        time.sleep(1)
        self.logger.do_click('SETTINGS')
        self.driver.find_element_by_xpath(self.PATH_UNIT_SETTINGS_BUTTON).click()
        time.sleep(1)
        if(line in variables.PATH_MAXIMUM_ATTEMPTS):
            self.logger.do_input('Maximum Attempts = "' + value + '"')
            self.driver.find_element_by_xpath(self.PATH_MAXIMUM_ATTEMPTS_FIELD).click()
            self.driver.find_element_by_xpath(self.PATH_MAXIMUM_ATTEMPTS_FIELD).send_keys(Keys.ARROW_LEFT)
            self.driver.find_element_by_xpath(self.PATH_MAXIMUM_ATTEMPTS_FIELD).send_keys(Keys.DELETE)
            self.driver.find_element_by_xpath(self.PATH_MAXIMUM_ATTEMPTS_FIELD).send_keys(value)
        elif(line in variables.PATH_SHOW_ANSWER):
            self.driver.find_element_by_xpath(self.PATH_SHOW_ANSWER_FIELD).send_keys(value)
        elif (line in variables.PATH_SHOW_RESET):
            self.driver.find_element_by_xpath(self.PATH_SHOW_RESET_FIELD).send_keys(value)

        time.sleep(1)
        self.click_save()
        self.logger.do_click('Publish')
        self.driver.find_element_by_xpath(self.PATH_PUBLISH_BUTTON).click()
        time.sleep(3)

    def set_unit_xblock_value(self, unit, filePath):
        '''Set content group'''
        if (unit not in self.driver.find_element_by_xpath("//ol[@class='list-sections is-sortable']").text):
            self.logger.do_click('Subsection')
            self.driver.find_element_by_xpath(self.PATH_SUBSECTION_BUTTON).click()
            time.sleep(1)
        self.logger.do_click('Unit')
        self.driver.find_element_by_xpath("//a[contains(text(), '" + unit + "')]").click()
        time.sleep(3)
        self.logger.do_click('EDIT')
        self.driver.find_element_by_xpath(self.PATH_EDIT_BUTTON).click()
        time.sleep(1)
        file = open(variables.PATH_TO_LIB + filePath, 'r')
        fileList = file.read()
        self.config.execute_script_input(self.PATH_XBLOCK_TEXT_FIELD, fileList)
        time.sleep(1)
        self.click_save()
        self.logger.do_click('Publish')
        self.driver.find_element_by_xpath(self.PATH_PUBLISH_BUTTON).click()
        time.sleep(3)
        self.logger.do_click('Section')
        self.driver.find_element_by_xpath(self.PATH_SECTION_BUTTON).click()
        time.sleep(3)



    def get_text_course_outline_text(self):
        '''Get text Course Outline'''
        return self.driver.find_element_by_xpath(self.PATH_COURSE_OUTLINE).text.replace('\n', '; ')

    def get_text_xblock_editor_text(self):
        '''Get text Xblock editor'''
        return self.driver.find_element_by_xpath(self.PATH_XBLOCK_EDITOR).text.replace('\n', '; ')

    def get_courses_groups_text(self):
        '''Get courses groups'''
        return self.driver.find_element_by_xpath(self.PATH_COURSES_GROUPS_TEXT).text

    def get_status_unit_visible(self):
        '''Get text Course Outline'''
        result = variables.STATUS_OFF
        if(self.driver.find_element_by_xpath(self.PATH_XBLOCK_EDITOR).is_selected()):
            result = variables.STATUS_ON
        return result





