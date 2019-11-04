"""
Enterprise Data Consent page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.enterprise.ent_course_enrollment_page import EnterpriseCourseEnrollment


class EnterpriseDataSharingConsentPage(PageObject):
    """
    Enterprise data consent page class
    """

    CONSENT_MSG_CSS = '.consent-message>p'

    url = None

    def is_browser_on_page(self):
        """
        Verifies if the data sharing consent
        title is visible on the page
        """
        return self.q(
            css='.consent-title'
        ).visible

    def get_consent_message_text(self):
        """
        Returns consent message text
        """
        return self.q(
            css='{}:nth-of-type(1)'.format(self.CONSENT_MSG_CSS)
        ).text[0]

    def get_enterprise_name_from_msg(self):
        """
        Returns enterprise name present in consent message
        """
        return self.q(
            css='{}:nth-of-type(1)>b'.format(self.CONSENT_MSG_CSS)
        ).text[0]

    def open_policy_text(self):
        """
        Click on the policy link to open policy text
        """
        self.q(css='#policy-dropdown-link').click()
        self.wait_for_element_visibility(
            '#consent-policy',
            "wait for policy text"
        )

    def get_consent_button_status(self):
        """

        Returns:
            Boolean: True if button is enabled
        """
        return self.q(
            css='#consent-button[disabled="disabled"]'
        ).present

    def accept_data_sharing_consent(self):
        """
        Check the data consent check box
        """
        self.q(css="#data-consent-checkbox").click()
        self.wait_for_element_absence(
            '#consent-button[disabled="disabled"]',
            'wait for consent button to get enabled'
        )
        self.q(css="#consent-button").click()

    def decline_data_sharing_consent(self):
        """
        Decline data sharing consent
        """
        self.q(css="#failure-link").click()
        self.wait_for_element_visibility(
            '#consent-confirmation-modal-content',
            'wait for consent pop up'
        )
        self.q(css="#modal-no-consent-button").click()
        EnterpriseCourseEnrollment(self.browser).wait_for_page()
