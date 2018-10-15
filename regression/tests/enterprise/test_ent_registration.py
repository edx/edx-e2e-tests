"""
Enterprise Registration tests
"""
from regression.tests.enterprise.ent_test_base import EnterpriseTestBase


class TestEnterpriseRegistration(EnterpriseTestBase):
    """
    Test Enterprise Registration
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestEnterpriseRegistration, self).setUp()
        self.browser.maximize_window()

    def test_enterprise_unlinked_user_registration(self):
        """
        Scenario: To verify that user is able to use enterprise portal to
        register into edX and link accounts
            Given a user does not have an edx account
            When this user logs in to the Enterprise portal
                And clicks on the course enrollment link
            Then the user is taken directly to edx customized logistration
            page
                And user can register here and go to course enrollment page
        """
        # The edX site is visited just to make sure that when user jumps to edX
        # from portal we don't have to handle authentication popup
        self.lms_login.visit()
        # Enterprise portal flow
        self.login_to_ent_portal(
            self.ENT_PORTAL_USERNAME,
            self.ENT_PORTAL_PASSWORD)
        self.access_course()
        self.ent_edx_login.wait_for_page()
        self.register_ent_edx_user()
        # Verify that user is on course enrollment page and correct course
        # is displayed there
        self.ent_course_enrollment.wait_for_page()
        self.assertEqual(
            self.ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
        # Call the fixture to unlink existing account for the user
        self.unlink_account()
