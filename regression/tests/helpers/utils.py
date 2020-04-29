"""
Test helper functions.
"""
from __future__ import absolute_import, print_function

import os
import uuid

import six
from six import text_type

from regression.pages.studio import LOGIN_BASE_URL
from regression.pages.studio.utils import get_course_key
from regression.pages.whitelabel.activate_account import ActivateAccount
from regression.pages.whitelabel.const import ORG, UNUSED_REGISTRATION_FIELDS_MAPPING

COURSE_ORG = 'COURSE_ORG'
COURSE_NUMBER = 'COURSE_NUMBER'
COURSE_RUN = 'COURSE_RUN'
COURSE_DISPLAY_NAME = 'COURSE_DISPLAY_NAME'


def get_random_credentials():
    """
    Get random user name and email address
    """
    username = 'test_{}'.format(str(uuid.uuid4().node))
    email = "{}@example.com".format(username)
    return username, email


def get_random_password():
    """
    Get random password, suitable for registering a user
    """
    # Allow specifying a prefix in case a site has specific complexity
    # requirements. But provide a default that should cover most cases.
    prefix = os.environ.get('NEW_PASSWORD_PREFIX', 'a0.')
    return prefix + uuid.uuid4().hex


def get_course_info():
    """
    Returns the course info of the course that we use for
    the regression tests.
    """
    return {
        'org': os.environ.get(COURSE_ORG),
        'number': os.environ.get(COURSE_NUMBER),
        'run': os.environ.get(COURSE_RUN),
        'display_name': os.environ.get(
            COURSE_DISPLAY_NAME)
    }


def get_wl_course_info(org, num, run):
    """
    Returns the course info of the course that we use for
    the wl regression tests.
    Arguments:
        org
        num
        run
    Returns:
        Course Info
    """
    return {
        'course_org': org,
        'course_num': num,
        'course_run': run,
        'display_name': "{}-{}-Test".format(org, num)
    }


def get_course_display_name():
    """
    Returns the course info of the course that we use for
    the regression tests.
    """
    return os.environ.get(COURSE_DISPLAY_NAME)


def visit_all(pages):
    """
    Visit each page object in `pages` (an iterable).
    Arguments:
        pages:
    """
    for page in pages:
        print("Visiting: {}".format(page))
        page.visit()


def get_url(url_path, course_info):
    """
    Construct a URL to the page within the course.
    Arguments:
        url_path:
        course_info:
    """
    course_key = get_course_key(course_info)
    return "/".join([LOGIN_BASE_URL, url_path, text_type(course_key)])


def get_data_locator(page):
    """
    Get Data locator
    Arguments:
        page:
    Returns:
        Unique data locator for the component
    """
    data_locator = page.q(css='.hd-3').attrs('id')[0]
    return data_locator


def get_data_id_of_component(page):
    """
    Get data id of component
    Arguments:
        page
    Returns:
        ID for the component
    """
    data_id = page.q(css='.problem-header').attrs('id')[0]
    return data_id


def get_white_label_registration_fields(
        email='', password='', name="Automated Test User",
        username='', first_name='Test', last_name='User',
        gender='m', year_of_birth='1994', state='Massachusetts',
        country='US', level_of_education='m', company='Arbisoft', title='SQA',
        profession='physician', specialty='neurology', terms_of_service="true",
        honor_code="true"
):
    """
    Returns a dictionary of fields to register a user.

    Arguments:
        email(str): User's email
        password(str): User's password
        name(str): User's full name
        first_name(str): User's first name
        last_name(str): User's last name
        gender(str): User's gender
        year_of_birth(str): User's year of birth
        state(str): User's current state of residence.
        country(str): User's country
        level_of_education(str): User's education level.
        company(str): User's current company  of affiliation.
        title(str): User's title.
        username(str): User's user name
        profession(str): Profession of user
        specialty(str): User's Area of specialty,
        terms_of_service(str): Terms of Services checkbox
        honor_code(str): Honor code check box

    Returns:
        dict: A dictionary of all fields.
    """
    # use the username and email values if set by function call, otherwise
    # set random values
    get_user_name, get_user_email = get_random_credentials()
    get_user_password = get_random_password()
    return {
        'email': email or get_user_email,
        'confirm_email': email or get_user_email,
        'username': username or get_user_name,
        'password': password or get_user_password,
        'name': name,
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'year_of_birth': year_of_birth,
        'state': state,
        'country': country,
        'level_of_education': level_of_education,
        'company': company,
        'title': title,
        'profession': profession,
        'specialty': specialty,
        'terms_of_service': terms_of_service,
        'honor_code': honor_code
    }


def fill_input_fields(page, elements_and_values_dict):
    """
    Fill input fields

    Arguments:
        page(PageObject): Page to fill input fields on.
        elements_and_values_dict(dict): A dictionary of
            elements(css) and input values.
    """
    for key, value in six.iteritems(elements_and_values_dict):
        page.q(css=key).fill(value)


def select_drop_down_values(page, elements_and_values_dict):
    """
    Select drop down values.

    Arguments:
        page(PageObject): Page on which drop down exists
        elements_and_values_dict(dict): A dictionary of
            drop down elements(css) and values.
    """
    for element, val in six.iteritems(elements_and_values_dict):
        target_css = 'select[name={}] option[value="{}"]'.format(element, val)
        page.wait_for_element_visibility(
            target_css,
            'target value is visible in Drop down'
        )
        page.q(css=target_css).click()


def click_checkbox(page, checkbox_css, toggle=False):
    """
    Click a checkbox.

    Arguments:
        page(PageObject): The page object on which checkbox exists.
        checkbox_css(str): The css of checkbox.
        toggle(bool): If False then, it won't un-check the checked checkbox.
    """
    page.wait_for_element_visibility(checkbox_css, 'wait for target checkbox')
    checkbox = page.q(css=checkbox_css).results[0]

    if toggle:
        checkbox.click()
    else:
        if not checkbox.is_selected():
            checkbox.click()


def activate_account(test, email_api):
    """
    Activates an account.

    Fetch activation url from email, open the activation link in a new
    window, verify that account is activated.

    Arguments:
        test: The browser on which activation is performed.
        email_api(GuerrillaMailApi): Api to access GuerrillaMail.
    """
    main_window = test.browser.current_window_handle
    # Get activation link from email
    activation_url = email_api.get_url_from_email(
        'activate'
    )
    # Open a new window and go to activation link in this window
    test.browser.execute_script("window.open('');")
    test.browser.switch_to.window(test.browser.window_handles[-1])
    account_activate_page = ActivateAccount(test.browser, activation_url)
    account_activate_page.visit()
    # Verify that activation is complete
    test.assertTrue(account_activate_page.is_account_activation_complete)
    test.browser.close()
    # Switch back to original window and refresh the page
    test.browser.switch_to.window(main_window)
    test.browser.refresh()


def get_org_specific_registration_fields():
    """
    Get ORG Specific registration fields by removing unused fields based on
    the selected ORG
    Returns:
        filtered registration data
    """
    registration_data = get_white_label_registration_fields()
    unused_field_keys = UNUSED_REGISTRATION_FIELDS_MAPPING[ORG]
    for field in unused_field_keys:
        registration_data.pop(field)
    return registration_data


def construct_course_basket_page_url(course_id):
    """
    Uses the course id to construct course related basket page url
    Arguments:
        course_id:
    Returns:
        constructed url:
    """
    return 'account/finish_auth?course_id={}&enrollment_action=enroll&' \
           'purchase_workflow=single&next=/dashboard'.format(course_id)
