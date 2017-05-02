"""
Test helper functions.
"""
import os

from regression.pages.studio.utils import get_course_key
from regression.pages.studio import LOGIN_BASE_URL
from regression.pages.whitelabel.activate_account import ActivateAccount

COURSE_ORG = 'COURSE_ORG'
COURSE_NUMBER = 'COURSE_NUMBER'
COURSE_RUN = 'COURSE_RUN'
COURSE_DISPLAY_NAME = 'COURSE_DISPLAY_NAME'


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


def get_course_display_name():
    """
    Returns the course info of the course that we use for
    the regression tests.
    """
    return os.environ.get(COURSE_DISPLAY_NAME)


def visit_all(pages):
    """
    Visit each page object in `pages` (an iterable).
    """
    for page in pages:
        print "Visiting: {}".format(page)
        page.visit()


def get_url(url_path, course_info):
    """
    Construct a URL to the page within the course.
    """
    course_key = get_course_key(course_info)
    return "/".join([LOGIN_BASE_URL, url_path, unicode(course_key)])


def get_data_locator(page):
    """
    Returns:
        Unique data locator for the component
    """
    data_locator = page.q(css='.hd-3').attrs('id')[0]
    return data_locator


def get_data_id_of_component(page):
    """
    Returns:
        ID for the component
    """
    data_id = page.q(css='.problem-header').attrs('id')[0]
    return data_id


def get_white_label_registration_fields(
        email='', password='', full_name='White label Test User',
        first_name='White Label', last_name='Test User', gender='m',
        yob='1994', state='Massachusetts', country='US', edu_level='m',
        company='Arbisoft', title='SQA', user_name=''

):
    """
    Returns a dictionary of fields to register a user.

    Arguments:
        email(str): User's email
        password(str): User's password
        full_name(str): User's full name
        first_name(str): User's first name
        last_name(str): User's last name
        gender(str): User's gender
        yob(str): User's year of birth
        state(str): User's current state of residence.
        country(str): User's country
        edu_level(str): User's education level.
        company(str): User's current company  of affiliation.
        title(str): User's title.
        user_name(str): User's user name

    Returns:
        dict: A dictionary of all fields.
    """
    return {
        'email': email,
        'password': password,
        'full_name': full_name,
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'yob': yob,
        'state': state,
        'country': country,
        'edu_level': edu_level,
        'company': company,
        'title': title,
        'user_name': user_name
    }


def fill_input_fields(page, elements_and_values_dict):
    """
    Fill input fields

    Arguments:
        page(PageObject): Page to fill input fields on.
        elements_and_values_dict(dict): A dictionary of
            elements(css) and input values.
    """
    for key, value in elements_and_values_dict.iteritems():
        page.q(css=key).fill(value)


def select_drop_down_values(page, elements_and_values_dict):
    """
    Select drop down values.

    Arguments:
        page(PageObject): Page on which drop down exists
        elements_and_values_dict(dict): A dictionary of
            drop down elements(css) and values.
    """
    for element, val in elements_and_values_dict.iteritems():
        page.wait_for_element_visibility(
            'select[name={}]'.format(element), 'Drop down is visible')
        page.q(
            css='select[name={}] option[value="{}"]'.format(element, val)
        ).click()


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
        browser(NeedleDriver): The browser on which activation is performed.
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
