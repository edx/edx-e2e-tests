"""
Student dashboard page.
"""
from edxapp_acceptance.pages.lms.dashboard import DashboardPage

from regression.pages.whitelabel.const import URL_WITH_AUTH


class DashboardPageExtended(DashboardPage):
    """
    This class is an extended class of Dashboard Page,
    where we add methods that are different or not used in DashboardPage
    """
    url = URL_WITH_AUTH + u'dashboard'

    def logout_lms(self):
        """
        Log-out from LMS
        """
        log_out_button_css = '.user-account li>a[href="/logout"]'
        self.q(css='.user-name').click()
        self.wait_for_element_visibility(
            log_out_button_css,
            'wait for user dropdown to expand'
        )
        self.q(css=log_out_button_css).click()

    @property
    def is_activation_message_present(self):
        """
        Returns 'True' if account activation message is present on dashboard
        """
        return self.q(css='.activation-message').present
