"""
User account page
"""
from __future__ import absolute_import

from selenium.webdriver.common.keys import Keys

from edxapp_acceptance.pages.lms.account_settings import AccountSettingsPage
from regression.pages.lms import LOGIN_BASE_URL


class UserAccountSettings(AccountSettingsPage):
    """
    This class is an extended class of AccountSettingsPage,
    where we add methods that are different or not used in AccountSettingsPage
    """

    url = LOGIN_BASE_URL + '/account/settings'

    IDP_PARTIAL_CSS_SELECTOR = '.u-field.u-field-social.u-field-auth-saml-'

    def is_idp_account_linked(self, idp_css_id):
        """
        Check if idp account is linked or not
        Arguments:
            idp_css_id
        Returns:
            Linked Status
        """
        return 'Unlink' in self.q(
            css=self.IDP_PARTIAL_CSS_SELECTOR + idp_css_id + ' a>.sr'
        ).text[0]

    def unlink_idp_account(self, idp_css_id):
        """
        Unlink idp account
        Arguments:
            idp_css_id
        """
        idp_css_selector = self.IDP_PARTIAL_CSS_SELECTOR + idp_css_id + ' a'
        self.q(css=idp_css_selector).click()
        self.wait_for(
            lambda:
            'Link' in self.q(css=idp_css_selector + '>.sr').text[0],
            'Wait for Link text to appear'
        )

    def fill_secondary_email_field(self, email):
        """
        Fill secondary email field
        Arguments:
            email
        """
        self.wait_for_element_visibility('#field-input-secondary_email', 'Secondary Email field is shown')
        elem = self.q(css='#field-input-secondary_email').results[0]
        elem.clear()
        elem.send_keys(email)
        elem.send_keys(Keys.ENTER)

    def get_user_email(self):
        """
        Get User email address
        """
        self.wait_for_element_visibility('#field-input-email', 'Primary Email Field visible')
        email_input = self.q(css='#field-input-email').results[0]
        return email_input.get_attribute('value')
