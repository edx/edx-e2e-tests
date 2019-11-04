"""
Enterprise Logistration page
"""
from __future__ import absolute_import

from edxapp_acceptance.pages.lms.login_and_register import CombinedLoginAndRegisterPage
from regression.pages.lms import LOGIN_BASE_URL


class EnterpriseEdxLogin(CombinedLoginAndRegisterPage):
    """
    This class is an extended class of CombinedLoginAndRegisterPage,
    where we add methods that are different or not used in LMS
    """
    url = LOGIN_BASE_URL + '/login'

    def is_browser_on_page(self):
        """
        Verifies if the enterprise logo is visible on the page
        """
        return self.q(css='.login-button').visible

    def get_enterprise_name(self):
        """
        Returns enterprise name
        """
        return self.q(css='.enterprise-logo').attrs('alt')[0]
