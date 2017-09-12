"""
Enterprise Enrollment Page tests
"""
from regression.pages.common.utils import (
    extract_mmm_dd_yyyy_date_string_from_text
)
from regression.tests.enterprise.enterprise_test_base import EnterpriseTestBase


class TestEnterpriseEnrollmentPage(EnterpriseTestBase):
    """
    Test Enterprise Login
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestEnterpriseEnrollmentPage, self).setUp()
        self.browser.maximize_window()

    def test_enrollment_verified_course(self):
        """
        Scenario: To verify that user sees the correct settings for verified
         course on enrollment landing page
            Given a user has an edx account which is linked to an Enterprise
                portal account
            When this user lands on the enrollment landing page
            Then this user is shown verified check box which is checked
            And unchecked Audit check box

        """
        # The edX site is visited just to make sure that when user jumps to
        # edX from portal we don't have to handle authentication popup
        self.lms_login.visit()
        # Enterprise portal flow
        self.login_to_enterprise_portal()
        self.access_course()
        self.login_enterprise_edx_user()
        # Verify that user is on course enrollment page and correct course
        # is displayed there
        self.enterprise_course_enrollment.wait_for_page()
        self.assertDictEqual(
            self.ENT_COURSE_TITLE,
            self.enterprise_course_enrollment.get_course_title()
        )
        # Verify that course type "verified" is present as a selectable option
        self.assertTrue(
            self.enterprise_course_enrollment.target_course_type_is_present(
                "verified"
            )
        )
        # Verify that course type "verified" option is checked
        self.assertTrue(
            self.enterprise_course_enrollment.target_course_type_is_checked(
                "verified"
            )
        )
        # Verify that course type "audit" is present as a selectable option
        self.assertTrue(
            self.enterprise_course_enrollment.target_course_type_is_present(
                "audit"
            )
        )

    def test_enrollment_course_info_and_detail(self):
        """
        Scenario: To verify that user sees the correct course info and detail
        on enrollment landing page
            Given a user has an edx account which is linked to an Enterprise
                portal account
            When this user lands on the enrollment landing page
            Then this user is shown correct course details
        """
        # The edX site is visited just to make sure that when user jumps to
        # edX from portal we don't have to handle authentication popup
        self.lms_login.visit()
        # Enterprise portal flow
        self.login_to_enterprise_portal()
        self.access_course()
        self.login_enterprise_edx_user()
        # Verify that user is on course enrollment page and correct course
        # is displayed there
        self.enterprise_course_enrollment.wait_for_page()
        # Verify Course Title on landing page
        self.assertDictEqual(
            self.ENT_COURSE_TITLE,
            self.enterprise_course_enrollment.get_course_title()
        )
        # Verify Course Org on landing page
        self.assertEqual(
            self.ENT_COURSE_ORG,
            self.enterprise_course_enrollment.get_course_org()
        )
        # Verify Course Start Date on landing page
        self.assertIn(
            self.ENT_COURSE_START_DATE,
            extract_mmm_dd_yyyy_date_string_from_text(
                self.enterprise_course_enrollment.get_course_info()
            )
        )
        # Fetch and verify Course Title and Org from details header
        course_title, course_org = \
            self.enterprise_course_enrollment.get_course_detail_headers()
        self.assertEqual(course_title, self.ENT_COURSE_TITLE)
        self.assertEqual(course_org, self.ENT_COURSE_ORG)
        # Fetch and verify Price from details body
        self.assertIn(
            self.ENT_COURSE_PRICE,
            self.enterprise_course_enrollment.get_course_detail_body()['price']
        )
