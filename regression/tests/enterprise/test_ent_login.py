"""
Enterprise Login tests
"""
from regression.tests.enterprise.ent_test_base import EntTestBase


class TestEntLogin(EntTestBase):
    """
    Test Enterprise Login
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestEntLogin, self).setUp()
        self.browser.maximize_window()

    def test_enterprise_login_linked_user(self):
        """
        Scenario: To verify that user is able to use enterprise portal to login
        linked edx account
            Given a user has an edx account which is linked to an Enterprise
                portal account
            When this user logs in to the Enterprise portal
                And clicks on the course enrollment link
            Then the user is taken directly to dashboard page without having
            to provide edx credentials
        """
        # The edX site is visited just to make sure that when user jumps to edX
        # from portal we don't have to handle authentication popup
        self.lms_login.visit()
        # Enterprise portal flow
        self.login_to_ent_portal()
        self.access_course()
        self.login_ent_edx_user()
        # Verify that user is on course enrollment page and correct course
        # is displayed there
        self.ent_course_enrollment.wait_for_page()
        self.assertDictEqual(
            self.ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )

    def test_enterprise_login_unlinked_user(self):
        """
        Scenario: To verify that user is able to use enterprise portal to
        login into edX and link accounts
            Given a user has an edx account which is not linked to an
            Enterprise
            When this user logs in to the Enterprise portal
                And clicks on the course enrollment link
            Then the user is taken directly to edx customized logistration
            page
                And user can provide edx credentials here to link both accounts
        """
        # Call the fixture to unlink any existing account for the user
        self.login_and_unlink_account()
        # Enterprise portal flow
        self.login_to_ent_portal()
        self.access_course()
        self.login_ent_edx_user()
        # Verify that user is on course enrollment page and correct course
        # is displayed there
        self.ent_course_enrollment.wait_for_page()
        self.assertDictEqual(
            self.ENT_COURSE_TITLE,
            self.ent_course_enrollment.get_course_title()
        )
