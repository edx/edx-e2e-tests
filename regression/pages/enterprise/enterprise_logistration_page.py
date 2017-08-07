"""
Enterprise Logistration page
"""
from edxapp_acceptance.pages.lms.login_and_register import (
    CombinedLoginAndRegisterPage
)


class EnterpriseLogistration(CombinedLoginAndRegisterPage):
    """
    This class is an extended class of CombinedLoginAndRegisterPage,
    where we add methods that are different or not used in LMS
    """

    def is_browser_on_page(self):
        """
        Verifies if the enterprise logo is visible on the page
        """
        return self.q(css='.enterprise-logo').visible

    def get_enterprise_name(self):
        """
        Returns enterprise name
        Returns:
            Enterprise Name
        """
        return self.q(css='.enterprise-logo').attrs('alt')[0]
