"""
Register page.
"""
from edxapp_acceptance.pages.lms.login_and_register import (
    CombinedLoginAndRegisterPage
)
from regression.pages.lms import BASE_URL


class RegisterPageExtended(CombinedLoginAndRegisterPage):
    """
    This class is an extended class of Register Page,
    where we add methods that are different or not used in Register Page
    """
    url = BASE_URL + "/register"
