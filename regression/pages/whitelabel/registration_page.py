"""
Registration page.
"""
import os

from edxapp_acceptance.pages.lms.login_and_register import (
    CombinedLoginAndRegisterPage
)
from edxapp_acceptance.tests.helpers import disable_animations
from regression.pages.whitelabel import ORG, LMS_URL_WITH_AUTH
from regression.tests.helpers.utils import (
    click_checkbox,
    fill_input_fields,
    select_drop_down_values,

)


class RegisterPageExtended(CombinedLoginAndRegisterPage):
    """
    This class is an extended class of Register Page,
    where we add methods that are different or not used in Register Page
    """
    url = os.path.join(LMS_URL_WITH_AUTH, "register")

    def register_white_label_user(self, registration_fields, submit=True):
        """
        Registers a whitelabel users for whitelabel tests.
        Arguments:
            registration_fields(dict): A dictionary of all fields to be filled.
            submit(bool): If True then registration form will be submitted.
        """
        disable_animations(self)
        self.wait_for_element_visibility(
            '.form-toggle[data-type="login"]', 'Registration form is visible.'
        )

        elements_and_values = {
            '#register-email': registration_fields['email'],
            '#register-name': registration_fields['name'],
            '#register-username': registration_fields['username'],
            '#register-password': registration_fields['password'],
            '#register-first_name': registration_fields['first_name'],
            '#register-last_name': registration_fields['last_name'],
            '#register-state': registration_fields['state']
        }
        fill_input_fields(self, elements_and_values)

        select_drop_down_values(
            self,
            {"#register-country": registration_fields['country']}
        )

        if ORG == 'MITxPRO':
            fill_input_fields(
                self,
                {
                    '#register-company': registration_fields['company'],
                    '#register-title': registration_fields['title']
                }
            )
            select_drop_down_values(
                self,
                {
                    "#register-year_of_birth": registration_fields[
                        'year_of_birth'
                    ],
                    "#register-gender": registration_fields['gender'],
                    "#register-level_of_education": registration_fields[
                        'level_of_education'
                    ]
                }
            )
            click_checkbox(self, '#register-honor_code')

        if ORG == 'HarvardMedGlobalAcademy':
            select_drop_down_values(
                self,
                {
                    "#register-profession": registration_fields['profession'],
                    "#register-specialty": registration_fields['specialty']
                }
            )

        click_checkbox(self, '#register-terms_of_service')

        if submit:
            self.q(css='.register-button').click()

    def toggle_to_login_page(self):
        """
        Toggle to login page
        """
        self.q(css='.form-toggle[data-type="login"]').click()
