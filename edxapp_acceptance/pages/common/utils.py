"""
Utility methods common to Studio and the LMS.
"""


import requests
import six
from bok_choy.javascript import js_defined
from bok_choy.promise import BrokenPromise, EmptyPromise, Promise
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from edxapp_acceptance.pages.lms.create_mode import ModeCreationPage
from edxapp_acceptance.pages.lms.track_selection import TrackSelectionPage


def sync_on_notification(page, style='default', wait_for_hide=False):
    """
    Sync on notifications but do not raise errors.

    A BrokenPromise in the wait_for probably means that we missed it.
    We should just swallow this error and not raise it for reasons including:
    * We are not specifically testing this functionality
    * This functionality is covered by unit tests
    * This verification method is prone to flakiness
      and browser version dependencies

    See classes in edx-platform:
     lms/static/sass/elements/_system-feedback.scss
    """
    hiding_class = 'is-hiding'
    shown_class = 'is-shown'

    def notification_has_class(style, el_class):
        """
        Return a boolean representing whether
        the notification has the class applied.
        """
        if style == 'mini':
            css_string = '.wrapper-notification-mini.{}'
        else:
            css_string = '.wrapper-notification-confirmation.{}'
        return page.q(css=css_string.format(el_class)).present

    # Wait for the notification to show.
    # This notification appears very quickly and maybe missed. Don't raise an error.
    try:
        page.wait_for(
            lambda: notification_has_class(style, shown_class),
            'Notification should have been shown.',
            timeout=5
        )
    except BrokenPromise as _err:
        pass

    # Now wait for it to hide.
    # This is not required for web page interaction, so not really needed.
    if wait_for_hide:
        page.wait_for(
            lambda: notification_has_class(style, hiding_class),
            'Notification should have hidden.'
        )


def click_css(page, css, source_index=0, require_notification=True):
    """
    Click the button/link with the given css and index on the specified page (subclass of PageObject).

    Will only consider elements that are displayed and have a height and width greater than zero.

    If require_notification is False (default value is True), the method will return immediately.
    Otherwise, it will wait for the "mini-notification" to appear and disappear.
    """
    def _is_visible(element):
        """Is the given element visible?"""
        # Only make the call to size once (instead of once for the height and once for the width)
        # because otherwise you will trigger a extra query on a remote element.
        return element.is_displayed() and all(size > 0 for size in six.itervalues(element.size))

    # Disable all animations for faster testing with more reliable synchronization
    disable_animations(page)
    # Click on the element in the browser
    page.q(css=css).filter(_is_visible).nth(source_index).click()

    if require_notification:
        sync_on_notification(page)

    # Some buttons trigger ajax posts
    # (e.g. .add-missing-groups-button as configured in split_test_author_view.js)
    # so after you click anything wait for the ajax call to finish
    page.wait_for_ajax()


def confirm_prompt(page, cancel=False, require_notification=None):
    """
    Ensures that a modal prompt and confirmation button are visible, then clicks the button. The prompt is canceled iff
    cancel is True.
    """
    page.wait_for_element_visibility('.prompt', 'Prompt is visible')
    confirmation_button_css = '.prompt .action-' + ('secondary' if cancel else 'primary')
    page.wait_for_element_visibility(confirmation_button_css, 'Confirmation button is visible')
    require_notification = (not cancel) if require_notification is None else require_notification
    click_css(page, confirmation_button_css, require_notification=require_notification)


def hover(browser, element):
    """
    Hover over an element.
    """
    ActionChains(browser).move_to_element(element).perform()


def enroll_user_track(browser, course_id, track):
    """
    Utility method to enroll a user in the audit or verified user track.  Creates and connects to the
    necessary pages. Selects the track and handles payment for verified.
    Supported tracks are 'verified' or 'audit'.
    """
    track_selection = TrackSelectionPage(browser, course_id)

    # Select track
    track_selection.visit()
    track_selection.enroll(track)


def add_enrollment_course_modes(browser, course_id, tracks):
    """
    Add the specified array of tracks to the given course.
    Supported tracks are `verified` and `audit` (all others will be ignored),
    and display names assigned are `Verified` and `Audit`, respectively.
    """
    for track in tracks:
        if track == 'audit':
            # Add an audit mode to the course
            ModeCreationPage(
                browser,
                course_id, mode_slug='audit',
                mode_display_name='Audit'
            ).visit()

        elif track == 'verified':
            # Add a verified mode to the course
            ModeCreationPage(
                browser, course_id, mode_slug='verified',
                mode_display_name='Verified', min_price=10
            ).visit()


def is_focused_on_element(browser, selector):
    """
    Check if the focus is on the element that matches the selector.
    """
    return browser.execute_script(u"return $('{}').is(':focus')".format(selector))


def disable_animations(page):
    """
    Disable jQuery and CSS3 animations.
    """
    disable_jquery_animations(page)
    disable_css_animations(page)


def enable_animations(page):
    """
    Enable jQuery and CSS3 animations.
    """
    enable_jquery_animations(page)
    enable_css_animations(page)


@js_defined('window.jQuery')
def disable_jquery_animations(page):
    """
    Disable jQuery animations.
    """
    page.browser.execute_script("jQuery.fx.off = true;")


@js_defined('window.jQuery')
def enable_jquery_animations(page):
    """
    Enable jQuery animations.
    """
    page.browser.execute_script("jQuery.fx.off = false;")


def disable_css_animations(page):
    """
    Disable CSS3 animations, transitions, transforms.
    """
    page.browser.execute_script(u"""
        var id = 'no-transitions';

        // if styles were already added, just do nothing.
        if (document.getElementById(id)) {
            return;
        }

        var css = [
                '* {',
                    '-webkit-transition: none !important;',
                    '-moz-transition: none !important;',
                    '-o-transition: none !important;',
                    '-ms-transition: none !important;',
                    'transition: none !important;',
                    '-webkit-transition-property: none !important;',
                    '-moz-transition-property: none !important;',
                    '-o-transition-property: none !important;',
                    '-ms-transition-property: none !important;',
                    'transition-property: none !important;',
                    '-webkit-transform: none !important;',
                    '-moz-transform: none !important;',
                    '-o-transform: none !important;',
                    '-ms-transform: none !important;',
                    'transform: none !important;',
                    '-webkit-animation: none !important;',
                    '-moz-animation: none !important;',
                    '-o-animation: none !important;',
                    '-ms-animation: none !important;',
                    'animation: none !important;',
                '}'
            ].join(''),
            head = document.head || document.getElementsByTagName('head')[0],
            styles = document.createElement('style');

        styles.id = id;
        styles.type = 'text/css';
        if (styles.styleSheet){
          styles.styleSheet.cssText = css;
        } else {
          styles.appendChild(document.createTextNode(css));
        }

        head.appendChild(styles);
    """)


def enable_css_animations(page):
    """
    Enable CSS3 animations, transitions, transforms.
    """
    page.browser.execute_script("""
        var styles = document.getElementById('no-transitions'),
            head = document.head || document.getElementsByTagName('head')[0];

        head.removeChild(styles)
    """)


def select_option_by_text(select_browser_query, option_text, focus_out=False):
    """
    Chooses an option within a select by text (helper method for Select's select_by_visible_text method).

    Wrap this in a Promise to prevent a StaleElementReferenceException
    from being raised while the DOM is still being rewritten
    """
    def select_option(query, value):
        """ Get the first select element that matches the query and select the desired value. """
        try:
            select = Select(query.first.results[0])
            select.select_by_visible_text(value)
            if focus_out:
                query.first.results[0].send_keys(Keys.TAB)
            return True
        except StaleElementReferenceException:
            return False

    msg = u'Selected option {}'.format(option_text)
    EmptyPromise(lambda: select_option(select_browser_query, option_text), msg).fulfill()


def get_selected_option_text(select_browser_query):
    """
    Returns the text value for the first selected option within a select.

    Wrap this in a Promise to prevent a StaleElementReferenceException
    from being raised while the DOM is still being rewritten
    """
    def get_option(query):
        """ Get the first select element that matches the query and return its value. """
        try:
            select = Select(query.first.results[0])
            return (True, select.first_selected_option.text)
        except StaleElementReferenceException:
            return (False, None)

    text = Promise(lambda: get_option(select_browser_query), 'Retrieved selected option text').fulfill()
    return text


def get_options(select_browser_query):
    """
    Returns all the options for the given select.
    """
    return Select(select_browser_query.first.results[0]).options


def select_option_by_value(browser_query, value, focus_out=False):
    """
    Selects a html select element by matching value attribute
    """
    select = Select(browser_query.first.results[0])
    select.select_by_value(value)

    def options_selected():
        """
        Returns True if all options in select element where value attribute
        matches `value`. if any option is not selected then returns False
        and select it. if value is not an option choice then it returns False.
        """
        all_options_selected = True
        has_option = False
        for opt in select.options:
            if opt.get_attribute('value') == value:
                has_option = True
                if not opt.is_selected():
                    all_options_selected = False
                    opt.click()
        if all_options_selected and not has_option:
            all_options_selected = False
        if focus_out:
            browser_query.first.results[0].send_keys(Keys.TAB)
        return all_options_selected

    # Make sure specified option is actually selected
    EmptyPromise(options_selected, "Option is selected").fulfill()


def is_option_value_selected(browser_query, value):
    """
    return true if given value is selected in html select element, else return false.
    """
    select = Select(browser_query.first.results[0])
    ddl_selected_value = select.first_selected_option.get_attribute('value')
    return ddl_selected_value == value


def element_has_text(page, css_selector, text):
    """
    Return true if the given text is present in the list.
    """
    text_present = False
    text_list = page.q(css=css_selector).text

    if text_list and (text in text_list):
        text_present = True

    return text_present


def click_and_wait_for_window(page, element):
    """
    To avoid a race condition, click an element that launces a new window, and
    wait for that window to launch.
    To check this, make sure the number of window_handles increases by one.

    Arguments:
    page (PageObject): Page object to perform method on
    element (WebElement): Clickable element that triggers the new window to open
    """
    num_windows = len(page.browser.window_handles)
    element.click()
    WebDriverWait(page.browser, 10).until(
        lambda driver: len(driver.window_handles) > num_windows
    )


def assert_link(test, expected_link, actual_link):
    """
    Assert that 'href' and text inside help DOM element are correct.

    Arguments:
        test: Test on which links are being tested.
        expected_link (dict): The expected link attributes.
        actual_link (dict): The actual link attribute on page.
    """
    test.assertEqual(expected_link['href'], actual_link.get_attribute('href'))
    test.assertEqual(expected_link['text'], actual_link.text)


def assert_opened_help_link_is_correct(test, url):
    """
    Asserts that url of browser when help link is clicked is correct.
    Arguments:
        test (AcceptanceTest): test calling this method.
        url (str): url to verify.
    """
    test.browser.switch_to_window(test.browser.window_handles[-1])
    WebDriverWait(test.browser, 10).until(lambda driver: driver.current_url == url)
    # Check that the URL loads. Can't do this in the browser because it might
    # be loading a "Maze Found" missing content page.
    response = requests.get(url)
    test.assertEqual(response.status_code, 200, u"URL {!r} returned {}".format(url, response.status_code))


def assert_side_bar_help_link(test, page, href, help_text, as_list_item=False, index=-1, close_window=True):
    """
    Asserts that help link in side bar is correct.

    It first checks the url inside anchor DOM element and
    then clicks to ensure that help opens correctly.

    Arguments:
    test (AcceptanceTest): Test object
    page (PageObject): Page object to perform tests on.
    href (str): The help link which we expect to see when it is opened.
    as_list_item (bool): Specifies whether help element is in one of the
                         'li' inside a sidebar list DOM element.
    index (int): The index of element in case there are more than
                 one matching elements.
    close_window(bool): Close the newly-opened help window before continuing
    """
    expected_link = {
        'href': href,
        'text': help_text
    }
    # Get actual anchor help element from the page.
    actual_link = page.get_side_bar_help_element_and_click_help(as_list_item=as_list_item, index=index)
    # Assert that 'href' and text are the same as expected.
    assert_link(test, expected_link, actual_link)
    # Assert that opened link is correct
    assert_opened_help_link_is_correct(test, href)
    # Close the help window if not kept open intentionally
    if close_window:
        close_help_window(page)


def close_help_window(page):
    """
    Closes the help window
    Args:
        page (PageObject): Page object to perform tests on.
    """
    browser_url = page.browser.current_url
    if browser_url.startswith('https://edx.readthedocs.io') or browser_url.startswith('http://edx.readthedocs.io'):
        page.browser.close()  # close only the current window
        page.browser.switch_to_window(page.browser.window_handles[0])
