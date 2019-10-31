"""
Enterprise Enrollment Page tests
"""
from __future__ import absolute_import

from regression.pages.common.utils import extract_mmm_dd_yyyy_date_string_from_text
from regression.pages.enterprise.enterprise_const import (
    ENT_COURSE_ORG, ENT_COURSE_PRICE,
    ENT_COURSE_START_DATE,
    ENT_COURSE_TITLE
)
from regression.tests.enterprise.ent_test_base import EnterpriseTestBase


class TestEnterpriseCourseEnrollmentPage(EnterpriseTestBase):
    """
    Test Enterprise Enrollment page
    """

    def test_enrollment_verified_course(self):
        """
        Scenario: To verify that user sees the correct settings for verified
         course on enrollment landing page
            Given a user has an edx account
            which will be linked to an Enterprise
            portal account
            When this user lands on the enrollment landing page
            Then this user is shown verified check box which is checked
            And unchecked Audit check box

        """
        self.login_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)

        self.assertEqual(
            ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        # Verify that course type "verified" is present as a selectable option
        self.assertTrue(
            self.ent_course_enrollment.target_course_type_is_present(
                "verified"
            )
        )
        # Verify that course type "verified" option is checked
        self.assertTrue(
            self.ent_course_enrollment.target_course_type_is_checked(
                "verified"
            )
        )
        # Verify that course type "audit" is present as a selectable option
        self.assertTrue(
            self.ent_course_enrollment.target_course_type_is_present(
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
        self.login_and_go_to_course_enrollment_page()
        # Call the fixture to unlink existing account for the user
        self.addCleanup(self.unlink_account)
        # Verify Course Title on landing page
        self.assertEqual(
            ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        # Verify Course Org on landing page
        self.assertEqual(
            ENT_COURSE_ORG,
            self.ent_course_enrollment.get_course_org()
        )
        # Verify Course Start Date on landing page

        self.assertIn(
            ENT_COURSE_START_DATE,
            extract_mmm_dd_yyyy_date_string_from_text(
                self.ent_course_enrollment.get_course_info()
            )
        )
        # Open course detail pop up
        self.ent_course_enrollment.open_course_detail_popup()
        # Fetch and verify Course Title and Org from details header
        course_title, course_org = \
            self.ent_course_enrollment.get_course_detail_headers()
        self.assertEqual(course_title, ENT_COURSE_TITLE)
        self.assertEqual(course_org, ENT_COURSE_ORG)
        # Fetch and verify Price from details body
        self.assertIn(
            ENT_COURSE_PRICE,
            self.ent_course_enrollment.get_course_detail_body()['Price']
        )
