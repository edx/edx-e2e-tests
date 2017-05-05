"""
Registration page.
"""
from edxapp_acceptance.pages.lms.login_and_register import (
    CombinedLoginAndRegisterPage
)

from regression.tests.helpers.utils import (
    fill_input_fields,
    select_drop_down_values,
    click_checkbox
)
from regression.pages.whitelabel.const import ORG, URL_WITH_AUTH


class RegisterPageExtended(CombinedLoginAndRegisterPage):
    """
    This class is an extended class of Register Page,
    where we add methods that are different or not used in Register Page
    """
    url = URL_WITH_AUTH + "register"

    def register_white_label_user(self, registration_fields, submit=True):
        """
        Registers a whitelabel users for whitelabel tests.

        Arguments:
            registration_fields(dict): A dictionary of all fields to be filled.
            submit(bool): If True then registration form will be submitted.
        """
        self.wait_for_element_visibility(
            '.register-form', 'Registration form is visible.'
        )

        elements_and_values = {
            '#register-email': registration_fields['email'],
            '#register-name': registration_fields['full_name'],
            '#register-username': registration_fields['user_name'],
            '#register-password': registration_fields['password'],
            '#register-first_name': registration_fields['first_name'],
            '#register-last_name': registration_fields['last_name'],
            '#register-state': registration_fields['state']
        }

        drop_down_names_and_values = {
            "country": registration_fields['country'],
            "year_of_birth": registration_fields['yob'],
        }

        fill_input_fields(self, elements_and_values)
        select_drop_down_values(self, drop_down_names_and_values)
        click_checkbox(self, '#register-terms_of_service')

        if ORG == 'MITProfessionalX':
            fill_input_fields(
                self,
                {
                    '#register-company': registration_fields['company'],
                    '#register-title': registration_fields['title']
                }
            )
            click_checkbox(self, '#register-honor_code')

        if ORG != 'HarvardMedGlobalAcademy':
            select_drop_down_values(
                self,
                {
                    "gender": registration_fields['gender'],
                    "level_of_education": registration_fields['edu_level']
                }
            )

        if submit:
            self.q(css='.register-button').click()