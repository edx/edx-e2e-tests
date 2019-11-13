import time
from selenium.webdriver.common.keys import Keys
from e2e.main.conf.config import Config
from e2e.main.conf.logger import Logger
from e2e.main.conf import variables

class StudentAdminPage():

    PATH_INSTRUCTOR_BUTTON = "//a[@href='/courses/" + variables.ID_BASE_COURSE + "/instructor'] | //a[contains(text(), 'Instructor')]"
    PATH_STUDENT_ADMIN_BUTTON = "//button[contains(text(), 'Student Admin')]"
    PATH_TABLE_TEXT = "//section[@id='student_admin']"

    PATH_GRADEBOOK_BUTTON = "//a[contains(text(), ' View Gradebook ')]"
    PATH_USERS_TABLE = "//section[@class='gradebook-content']"
    PATH_EMAIL_FOR_PROGRESS_FIELD = "//input[@name='student-select-progress']"
    PATH_VIEW_PROGRESS_BUTTON = "//a[contains(text(), 'View Progress Page')]"

    PATH_STUDENT_EMAIL_FIELD = "//input[@name='student-select-grade']"
    PATH_PROBLEM_LOCATION_FIELD = "//input[@name='problem-select-single']"
    PATH_RESET_ATTEMPT_BUTTON = "//input[@name='reset-attempts-single']"
    PATH_RESCORE_LEARNERS_SUBMISSION_BUTTON = "//input[@name='rescore-problem-single']"
    PATH_RESCORE_LEARNERS_SUBMISSION_IMPROVES_BUTTON = "//input[@name='rescore-problem-if-higher-single']"
    PATH_OVERRIDE_LEARNERS_SCORE_FIELD = "//input[@name='score-select-single']"
    PATH_OVERRIDE_LEARNERS_SCORE_BUTTON = "//input[@name='override-problem-score-single']"
    PATH_DELETE_STATE_BUTTON = "//input[@name='delete-state-single']"
    PATH_SHOW_TASK_STATUS_BUTTON = "//input[@name='task-history-single']"

    PATH_ALL_PROBLEM_LOCATION_FIELD = "//input[@name='problem-select-all']"
    PATH_RESET_ALL_ATTEMPT_BUTTON = "//input[@name='reset-attempts-all']"
    PATH_SHOW_ALL_TASK_STATUS_BUTTON = "//input[@name='task-history-all']"
    PATH_RESCORE_ALL_LEARNERS_SUBMISSION_BUTTON = "//input[@name='rescore-problem-all']"
    PATH_RESCORE_ALL_LEARNERS_SUBMISSION_IMPROVES_BUTTON = "//input[@name='rescore-problem-all-if-higher']"

    def __init__(self, driver, *args, **kwargs):
        super(StudentAdminPage, self).__init__(*args, **kwargs)
        self.driver = driver
        self.logger = Logger()
        self.config = Config(self.driver)



    def open_student_admin(self):
        '''Open studen t admin'''
        self.logger.do_click('Instructor')
        self.config.execute_script_click(self.PATH_INSTRUCTOR_BUTTON)
        time.sleep(1)
        self.config.switch_window(0)
        time.sleep(1)
        self.logger.do_click('Student admin')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_ADMIN_BUTTON).click()
        time.sleep(3)

    def open_gradebook(self):
        '''Open membership'''
        driver = self.driver
        self.logger.do_click('Gradebook')
        driver.find_element_by_xpath(StudentAdminPage.PATH_GRADEBOOK_BUTTON).click()
        time.sleep(1)

    def open_learners_progress(self, email):
        '''Open learners progress'''
        self.logger.do_input('Learners email for progress = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FOR_PROGRESS_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_EMAIL_FOR_PROGRESS_FIELD).send_keys(email)
        self.logger.do_click('View Progress Page')
        self.driver.find_element_by_xpath(self.PATH_VIEW_PROGRESS_BUTTON).click()
        time.sleep(1)

    def reset_attempts(self, email, problem):
        '''Reset attempts'''
        self.logger.do_input('Learners email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Reset attempts to zero')
        self.driver.find_element_by_xpath(self.PATH_RESET_ATTEMPT_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def rescore_learners_submission(self, email, problem):
        '''Rescore learners submission'''
        self.logger.do_input('Learners email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Rescore learners submission')
        self.driver.find_element_by_xpath(self.PATH_RESCORE_LEARNERS_SUBMISSION_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def rescore_learners_submission_improves(self, email, problem):
        '''Rescore learners submission improves'''
        self.logger.do_input('Learners email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Rescore only if score improves')
        self.driver.find_element_by_xpath(self.PATH_RESCORE_LEARNERS_SUBMISSION_IMPROVES_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def override_learners_score(self,email, problem, score):
        '''Reset attempts'''
        self.logger.do_input('Learners email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_input('Score = "' + score + '"')
        self.driver.find_element_by_xpath(self.PATH_OVERRIDE_LEARNERS_SCORE_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_OVERRIDE_LEARNERS_SCORE_FIELD).send_keys(score)
        self.logger.do_click('Override Learners Score')
        self.driver.find_element_by_xpath(self.PATH_OVERRIDE_LEARNERS_SCORE_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def delete_learners_state(self, email, problem):
        '''Delete learners state'''
        self.logger.do_input('Learners email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Delete learners state')
        self.driver.find_element_by_xpath(self.PATH_DELETE_STATE_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def show_task_status(self, email, problem):
        '''Delete learners state'''
        self.logger.do_input('Learners email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Delete learners state')
        self.driver.find_element_by_xpath(self.PATH_SHOW_TASK_STATUS_BUTTON).click()
        time.sleep(3)



    def reset_all_attempts(self, problem):
        '''Reset attempts'''
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Reset attempts to zero')
        self.driver.find_element_by_xpath(self.PATH_RESET_ALL_ATTEMPT_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def rescore_all_learners_submission(self, problem):
        '''Rescore learners all submission'''
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Rescore learners submission')
        self.driver.find_element_by_xpath(self.PATH_RESCORE_ALL_LEARNERS_SUBMISSION_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def rescore_all_learners_submission_improves(self, problem):
        '''Rescore learners all submission improves'''
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Rescore only if scoresn improve for all learners')
        self.driver.find_element_by_xpath(self.PATH_RESCORE_ALL_LEARNERS_SUBMISSION_IMPROVES_BUTTON).click()
        time.sleep(1)
        try:
            self.driver.switch_to_alert().accept()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
            time.sleep(1)
        except:
            pass

    def show_all_task_status(self, problem):
        '''Delete learners state'''
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_ALL_PROBLEM_LOCATION_FIELD).send_keys(problem)
        self.logger.do_click('Show task status')
        self.driver.find_element_by_xpath(self.PATH_SHOW_ALL_TASK_STATUS_BUTTON).click()
        time.sleep(1)



    def delete_all_learners_score(self, email, problem):
        '''Delete learners score'''
        self.logger.do_input('Learners email = "' + email + '"')
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_STUDENT_EMAIL_FIELD).send_keys(email)
        self.logger.do_input('Problem location = "' + problem + '"')
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).clear()
        self.driver.find_element_by_xpath(self.PATH_PROBLEM_LOCATION_FIELD).send_keys(problem)
        try:
            self.logger.do_click('Reset attempts to zero')
            self.driver.find_element_by_xpath(self.PATH_RESET_ATTEMPT_BUTTON).click()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
        except:
            pass
        try:
            self.logger.do_click('Delete learners state')
            self.driver.find_element_by_xpath(self.PATH_DELETE_STATE_BUTTON).click()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
        except:
            pass
        time.sleep(3)
        self.driver.find_element_by_xpath(self.PATH_RESET_ATTEMPT_BUTTON).send_keys(Keys.PAGE_UP)
        time.sleep(1)



    def get_page_text(self):
        '''Get page text'''
        return self.driver.find_element_by_xpath(StudentAdminPage.PATH_TABLE_TEXT).text.replace('\n', '; ')

    def get_users_list_text(self):
        '''Get users'''
        return self.driver.find_element_by_xpath(StudentAdminPage.PATH_USERS_TABLE).text.replace('\n', '; ')


