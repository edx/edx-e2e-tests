from e2e.main.conf import variables
from e2e.main.conf.logger import Logger
from e2e.main.pages.admin.admin_page import AdminPage
from e2e.main.pages.cms.advanced_settings_page import AdvancedSettingsPage
from e2e.main.pages.cms.certificates_cms_page import CertificatesCmsPage
from e2e.main.pages.cms.import_page import ImportPage
from e2e.main.pages.lms.instructor.certificates_lms_page import CertificatesLmsPage
from e2e.main.pages.lms.course_page import CoursePage
from e2e.main.pages.cms.course_outline_page import CourseOutlinePage
from e2e.main.pages.lms.dashboard_page import DashboardPage
from e2e.main.pages.cms.grading_page import GradingPage
from e2e.main.pages.lms.instructor.student_admin_page import StudentAdminPage
from e2e.main.pages.lms.progress_page import ProgressPage
from e2e.main.pages.login_page import LoginPage
from e2e.main.pages.lms.instructor.membership_page import MembershipPage
from e2e.main.pages.cms.shedule_details_page import SheduleDetailsPage
from e2e.main.pages.lms.sysadmin.sysadmin_page import SysadminPage
from e2e.main.tests.main_class import MainClass
from e2e.main.conf.config import Config

class TestCertificate(MainClass):
    '''
        Pre-condition: Absent
        Past-condition:
            test_04_delete_created_course_modes
        '''

    def setUp(self):
        super(TestCertificate, self).setUp()
        self.logger = Logger()
        self.config = Config(self.driver)
        self.login_page = LoginPage(self.driver)
        self.advanced_settings_page = AdvancedSettingsPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.membership_page = MembershipPage(self.driver)
        self.shedule_details_page = SheduleDetailsPage(self.driver)
        self.course_outline_page = CourseOutlinePage(self.driver)
        self.course_page = CoursePage(self.driver)
        self.grading_page = GradingPage(self.driver)
        self.certificates_lms_page = CertificatesLmsPage(self.driver)
        self.certificates_cms_page = CertificatesCmsPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        self.sysadmin_page = SysadminPage(self.driver)
        self.progress_page = ProgressPage(self.driver)
        self.import_page = ImportPage(self.driver)
        self.student_admin_page = StudentAdminPage(self.driver)

    def test_01_course_certificate_creation(self):
        '''Course certificate creation'''
        self.logger.do_test_name("Course certificate creation")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.set_certificate_generation(variables.STATUS_ON)
        self.admin_page.set_certificate_html(variables.STATUS_ON)
        self.admin_page.open_course_modes()
        self.admin_page.filter_for_admin(variables.ORGANIZATION)
        self.admin_page.delete_activity_admin(variables.TEXT_DELETE_SELECTED_COURSE_MODES)
        self.admin_page.set_course_modes(courseId, variables.STATUS_MODE_HONOR, variables.TEXT_TEST)
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.certificates_cms_page.open_certificates()
        self.certificates_cms_page.setup_certificate()
        self.config.do_assert_true(variables.CERTIFICATE_DETAILS, self.certificates_cms_page.get_certificate_details_text())

    def test_02_preview_certificate(self):
        '''Preview Certificate'''
        self.logger.do_test_name("Preview Certificate")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.set_certificate_generation(variables.STATUS_ON)
        self.admin_page.set_certificate_html(variables.STATUS_ON)
        self.admin_page.open_course_modes()
        self.admin_page.filter_for_admin(variables.ORGANIZATION)
        self.admin_page.delete_activity_admin(variables.TEXT_DELETE_SELECTED_COURSE_MODES)
        self.admin_page.set_course_modes(courseId, variables.STATUS_MODE_HONOR, variables.TEXT_TEST)
        self.admin_page.logout()

        if (variables.PROJECT not in variables.PROJECT_ASUOSPP):
            self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.certificates_cms_page.open_certificates()
        self.certificates_cms_page.setup_certificate()
        self.certificates_cms_page.activate_certificate()
        self.certificates_cms_page.click_preview()
        self.config.switch_window(1)
        if (variables.PROJECT in variables.PROJECT_GIJIMA):
            self.login_page.input_email(variables.LOGIN_EMAIL_STAFF)
            self.login_page.input_password(variables.LOGIN_PASSWORD_STAFF)
            self.login_page.click_login_button()
        self.config.do_assert_true_in(variables.COURSE_NAME, self.certificates_cms_page.get_certificate_includes_text())
        self.config.do_assert_true_in(variables.ORGANIZATION, self.certificates_cms_page.get_certificate_includes_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.certificates_cms_page.get_certificate_includes_text())
        self.config.do_assert_true_in(variables.ROLE_STAFF, self.certificates_cms_page.get_certificate_includes_text())

    def test_03_request_certificate_view_certificate(self):
        '''Request Certificate/View Certificate'''
        self.logger.do_test_name("Request Certificate/View Certificate")
        courseId = variables.ID + variables.ORGANIZATION + "+" + variables.COURSE_NUMBER_POSITIVE + "+" + variables.COURSE_RUN

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.import_page.open_import()
        self.import_page.import_course(variables.COURSE_NONE)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_ADMIN, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.set_certificate_generation(variables.STATUS_ON)
        self.admin_page.set_certificate_html(variables.STATUS_ON)
        self.admin_page.open_course_modes()
        self.admin_page.filter_for_admin(variables.ORGANIZATION)
        self.admin_page.delete_activity_admin(variables.TEXT_DELETE_SELECTED_COURSE_MODES)
        self.admin_page.set_course_modes(courseId, variables.STATUS_MODE_HONOR, variables.TEXT_TEST)
        self.admin_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_CMS)
        self.course_outline_page.open_created_course(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.certificates_cms_page.open_certificates()
        self.certificates_cms_page.setup_certificate()
        self.certificates_cms_page.activate_certificate()
        self.advanced_settings_page.open_advanced_settings()
        self.advanced_settings_page.set_value_advanced_setting(variables.PATH_CERTIFICATES_DISPLAY_BEHAVIOR,
                                                               variables.EARLY_NO_INFO)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE,
                                                     variables.COURSE_RUN)
        self.student_admin_page.open_student_admin()
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_1)
        self.student_admin_page.delete_all_learners_score(variables.LOGIN_EMAIL_FIRST, variables.ID_UNIT_2)
        self.certificates_lms_page.open_certificates()
        self.certificates_lms_page.set_certificates(variables.STATUS_ON)
        self.dashboard_page.logout()

        self.login_page.login(variables.LOGIN_EMAIL_FIRST, variables.LOGIN_PASSWORD, variables.STATUS_LMS)
        self.dashboard_page.open_created_cours(variables.ORGANIZATION, variables.COURSE_NUMBER_POSITIVE, variables.COURSE_RUN)
        self.course_page.open_course()
        self.course_page.correct_answer_unit(1)
        self.course_page.correct_answer_unit(2)
        self.progress_page.open_progress()
        self.progress_page.click_request_certificate()
        self.progress_page.click_view_certificate()
        self.config.switch_window(1)
        self.config.do_assert_true_in(variables.COURSE_NAME, self.progress_page.get_certificate_text())
        self.config.do_assert_true_in(variables.ORGANIZATION, self.progress_page.get_certificate_text())
        self.config.do_assert_true_in(variables.COURSE_NUMBER_POSITIVE, self.progress_page.get_certificate_text())
        self.config.do_assert_true_in(variables.FULL_NAME, self.progress_page.get_certificate_text())

    def test_04_delete_created_course_modes(self):
        '''Delete created course modes'''
        self.login_page.login(variables.LOGIN_EMAIL_STAFF, variables.LOGIN_PASSWORD_STAFF, variables.STATUS_ADMIN)
        self.admin_page.open_course_modes()
        self.admin_page.filter_for_admin(variables.ORGANIZATION)
        self.admin_page.delete_activity_admin(variables.TEXT_DELETE_SELECTED_COURSE_MODES)




