"""
Helper methods for writing robust Selenium tests.

This extra safety basically comes from:

    1) Explicitly waiting for DOM and JavaScript changes
       (NEVER waiting for a pre-determined amount of time)

    2) Retrying on common exceptions.

There is no magic bullet for writing robust Selenium tests,
but these methods provide a solid foundation.
"""
import time
import json
from textwrap import dedent

from selenium.common.exceptions import (
    WebDriverException, StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from nose.tools import assert_true


class RequireJSError(Exception):
    """
    An error related to waiting for require.js. If require.js is unable to load
    a dependency in the `wait_for_requirejs` function, Python will throw
    this exception to make sure that the failure doesn't pass silently.
    """
    pass


class SafeSelenium(object):
    """
    Helper methods for robust Selenium tests.
    """

    IMPLICIT_WAIT = 0
    browser = None

    def __init__(self, browser):
        """
        Initialize the helpers to use `browser`
        (a `splinter.Browser` instance).
        """
        self.browser = browser

    def retry_on_exception(self, func, max_attempts=5, ignored_exceptions=StaleElementReferenceException):
        """
        Retry the interaction, ignoring the passed exceptions.
        By default ignore StaleElementReferenceException, which happens often in our application
        when the DOM is being manipulated by client side JS.
        Note that ignored_exceptions is passed directly to the except block, and as such can be
        either a single exception or multiple exceptions as a parenthesized tuple.
        """
        attempt = 0
        while attempt < max_attempts:
            try:
                return func()
            except ignored_exceptions:
                time.sleep(1)
                attempt += 1

        assert_true(attempt < max_attempts, 'Ran out of attempts to execute {}'.format(func))

    def wait_for(self, func, timeout=5, timeout_msg=None):
        """
        Calls the method provided with the driver as an argument until the
        return value is not False.
        Throws an error if the WebDriverWait timeout clock expires.
        Otherwise this method will return None.
        """
        msg = timeout_msg or "Timed out after {} seconds.".format(timeout)
        try:
            WebDriverWait(
                driver=self.browser.driver,
                timeout=timeout,
                ignored_exceptions=(StaleElementReferenceException)
            ).until(func)
        except TimeoutException:
            raise TimeoutException(msg)

    def is_css_present(self, css_selector, wait_time=10):
        return self.browser.is_element_present_by_css(css_selector, wait_time=wait_time)

    def is_css_not_present(self, css_selector, wait_time=5):
        self.browser.driver.implicitly_wait(1)
        try:
            return self.browser.is_element_not_present_by_css(css_selector, wait_time=wait_time)
        except:
            raise
        finally:
            self.browser.driver.implicitly_wait(self.IMPLICIT_WAIT)

    def css_has_text(self, css_selector, text, index=0, strip=False):
        """
        Return a boolean indicating whether the element with `css_selector`
        has `text`.

        If `strip` is True, strip whitespace at beginning/end of both
        strings before comparing.

        If there are multiple elements matching the css selector,
        use `index` to indicate which one.
        """
        # If we're expecting a non-empty string, give the page
        # a chance to fill in text fields.
        if text:
            self.wait_for(lambda _: self.css_text(css_selector, index=index))

        actual_text = self.css_text(css_selector, index=index)

        if strip:
            actual_text = actual_text.strip()
            text = text.strip()

        return actual_text == text

    def css_has_value(self, css_selector, value, index=0):
        """
        Return a boolean indicating whether the element with
        `css_selector` has the specified `value`.

        If there are multiple elements matching the css selector,
        use `index` to indicate which one.
        """
        # If we're expecting a non-empty string, give the page
        # a chance to fill in values
        if value:
            self.wait_for(lambda _: self.css_value(css_selector, index=index))

        return self.css_value(css_selector, index=index) == value

    def css_find(self, css, wait_time=30):
        """
        Wait for the element(s) as defined by css locator
        to be present.

        This method will return a WebDriverElement.
        """
        self.wait_for_present(css_selector=css, timeout=wait_time)
        return self.browser.find_by_css(css)

    def css_click(self, css_selector, index=0, wait_time=30):
        """
        Perform a click on a CSS selector, first waiting for the element
        to be present and clickable.

        This method will return True if the click worked.
        """
        self.wait_for_clickable(css_selector, timeout=wait_time)
        self.wait_for_visible(css_selector, index=index, timeout=wait_time)
        assert_true(
            self.css_visible(css_selector, index=index),
            msg="Element {}[{}] is present but not visible".format(css_selector, index)
        )

        result = self.retry_on_exception(lambda: self.css_find(css_selector)[index].click())
        return result

    def css_check(self, css_selector, wait_time=30):
        """
        Checks a check box based on a CSS selector, first waiting for the element
        to be present and clickable. This is just a wrapper for calling "click"
        because that's how selenium interacts with check boxes and radio buttons.

        Then for synchronization purposes, wait for the element to be checked.
        This method will return True if the check worked.
        """
        self.css_click(css_selector=css_selector, wait_time=wait_time)
        self.wait_for(lambda _: self.css_find(css_selector).selected)
        return True

    def select_option(self, name, value, wait_time=30):
        """
        A method to select an option
        Then for synchronization purposes, wait for the option to be selected.
        This method will return True if the selection worked.
        """
        select_css = "select[name='{}']".format(name)
        option_css = "option[value='{}']".format(value)

        css_selector = "{} {}".format(select_css, option_css)
        self.css_click(css_selector=css_selector, wait_time=wait_time)
        self.wait_for(lambda _: self.css_has_value(select_css, value))
        return True

    def css_fill(self, css_selector, text, index=0):
        """
        Set the value of the element to the specified text.
        Note that this will replace the current value completely.
        Then for synchronization purposes, wait for the value on the page.
        """
        self.wait_for_visible(css_selector, index=index)
        self.retry_on_exception(lambda: self.css_find(css_selector)[index].fill(text))
        self.wait_for(lambda _: self.css_has_value(css_selector, text, index=index))
        return True

    def click_link(self, partial_text, index=0):
        self.retry_on_exception(lambda: self.browser.find_link_by_partial_text(partial_text)[index].click())

    def click_link_by_text(self, text, index=0):
        self.retry_on_exception(lambda: self.browser.find_link_by_text(text)[index].click())

    def css_text(self, css_selector, index=0, timeout=30):
        # Wait for the css selector to appear
        if self.is_css_present(css_selector):
            return self.retry_on_exception(lambda: self.css_find(css_selector, wait_time=timeout)[index].text)
        else:
            return ""

    def css_value(self, css_selector, index=0):
        # Wait for the css selector to appear
        if self.is_css_present(css_selector):
            return self.retry_on_exception(lambda: self.css_find(css_selector)[index].value)
        else:
            return ""

    def css_html(self, css_selector, index=0):
        """
        Returns the HTML of a css_selector
        """
        assert_true(self.is_css_present(css_selector))
        return self.retry_on_exception(lambda: self.css_find(css_selector)[index].html)

    def css_has_class(self, css_selector, class_name, index=0):
        return self.retry_on_exception(lambda: self.css_find(css_selector)[index].has_class(class_name))

    def css_visible(self, css_selector, index=0):
        assert_true(self.is_css_present(css_selector))
        return self.retry_on_exception(lambda: self.css_find(css_selector)[index].visible)

    def wait_for_present(self, css_selector, timeout=30):
        """
        Wait for the element to be present in the DOM.
        """
        self.wait_for(
            func=lambda _: EC.presence_of_element_located((By.CSS_SELECTOR, css_selector,)),
            timeout=timeout,
            timeout_msg="Timed out waiting for {} to be present.".format(css_selector)
        )

    def wait_for_visible(self, css_selector, index=0, timeout=30):
        """
        Wait for the element to be visible in the DOM.
        """
        self.wait_for(
            func=lambda _: self.css_visible(css_selector, index),
            timeout=timeout,
            timeout_msg="Timed out waiting for {} to be visible.".format(css_selector)
        )

    def wait_for_invisible(self, css_selector, timeout=30):
        """
        Wait for the element to be either invisible or not present on the DOM.
        """
        self.wait_for(
            func=lambda _: EC.invisibility_of_element_located((By.CSS_SELECTOR, css_selector,)),
            timeout=timeout,
            timeout_msg="Timed out waiting for {} to be invisible.".format(css_selector)
        )

    def wait_for_clickable(self, css_selector, timeout=30):
        """
        Wait for the element to be present and clickable.
        """
        self.wait_for(
            func=lambda _: EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector,)),
            timeout=timeout,
            timeout_msg="Timed out waiting for {} to be clickable.".format(css_selector)
        )

    # Selenium's `execute_async_script` function pauses Selenium's execution
    # until the browser calls a specific Javascript callback; in effect,
    # Selenium goes to sleep until the JS callback function wakes it back up again.
    # This callback is passed as the last argument to the script. Any arguments
    # passed to this callback get returned from the `execute_async_script`
    # function, which allows the JS to communicate information back to Python.
    # Ref: https://selenium.googlecode.com/svn/trunk/docs/api/dotnet/html/M_OpenQA_Selenium_IJavaScriptExecutor_ExecuteAsyncScript.htm
    def wait_for_js_variable_truthy(self, variable):
        """
        Using Selenium's `execute_async_script` function, poll the Javascript
        environment until the given variable is defined and truthy. This process
        guards against page reloads, and seamlessly retries on the next page.
        """
        javascript = """
            var callback = arguments[arguments.length - 1];
            var unloadHandler = function() {{
              callback("unload");
            }}
            addEventListener("beforeunload", unloadHandler);
            addEventListener("unload", unloadHandler);
            var intervalID = setInterval(function() {{
              try {{
                if({variable}) {{
                  clearInterval(intervalID);
                  removeEventListener("beforeunload", unloadHandler);
                  removeEventListener("unload", unloadHandler);
                  callback(true);
                }}
              }} catch (e) {{}}
            }}, 10);
        """.format(variable=variable)
        for _ in range(5):  # 5 attempts max
            try:
                result = self.browser.driver.execute_async_script(dedent(javascript))
            except WebDriverException as wde:
                if "document unloaded while waiting for result" in wde.msg:
                    result = "unload"
                else:
                    raise
            if result == "unload":
                # we ran this on the wrong page. Wait a bit, and try again, when the
                # browser has loaded the next page.
                time.sleep(1)
                continue
            else:
                return result

    def wait_for_requirejs(self, dependencies):
        """
        If requirejs is loaded on the page, this function will pause
        Selenium until require is finished loading the given dependencies.
        If requirejs is not loaded on the page, this function will return
        immediately.

        :param dependencies: a list of strings that identify resources that
            we should wait for requirejs to load. By default, requirejs will only
            wait for jquery.
        """
        if not dependencies:
            dependencies = ["jquery"]
        # stick jquery at the front
        if dependencies[0] != "jquery":
            dependencies.insert(0, "jquery")

        javascript = """
            var callback = arguments[arguments.length - 1];
            if(window.require) {{
              requirejs.onError = callback;
              var unloadHandler = function() {{
                callback("unload");
              }}
              addEventListener("beforeunload", unloadHandler);
              addEventListener("unload", unloadHandler);
              require({deps}, function($) {{
                setTimeout(function() {{
                  removeEventListener("beforeunload", unloadHandler);
                  removeEventListener("unload", unloadHandler);
                  callback(true);
                }}, 50);
              }});
            }} else {{
              callback(false);
            }}
        """.format(deps=json.dumps(dependencies))
        for _ in range(5):  # 5 attempts max
            try:
                result = self.browser.driver.execute_async_script(dedent(javascript))
            except WebDriverException as wde:
                if "document unloaded while waiting for result" in wde.msg:
                    result = "unload"
                else:
                    raise
            if result == "unload":
                # we ran this on the wrong page. Wait a bit, and try again, when the
                # browser has loaded the next page.
                time.sleep(1)
                continue
            elif result not in (None, True, False):
                # We got a require.js error
                # Sometimes requireJS will throw an error with requireType=require
                # This doesn't seem to cause problems on the page, so we ignore it
                if result['requireType'] == 'require':
                    time.sleep(1)
                    continue

                # Otherwise, fail and report the error
                else:
                    msg = "Error loading dependencies: type={0} modules={1}".format(
                        result['requireType'], result['requireModules'])
                    err = RequireJSError(msg)
                    err.error = result
                    raise err
            else:
                return result

    def wait_for_ajax_complete(self):
        """
        Wait until all jQuery AJAX calls have completed. "Complete" means that
        either the server has sent a response (regardless of whether the response
        indicates success or failure), or that the AJAX call timed out waiting for
        a response. For more information about the `jQuery.active` counter that
        keeps track of this information, go here:
        http://stackoverflow.com/questions/3148225/jquery-active-function#3148506
        """
        javascript = """
            var callback = arguments[arguments.length - 1];
            if(!window.jQuery) {callback(false);}
            var intervalID = setInterval(function() {
              if(jQuery.active == 0) {
                clearInterval(intervalID);
                callback(true);
              }
            }, 100);
        """
        # Sometimes the ajax when it returns will make the browser reload
        # the DOM, and throw a WebDriverException with the message:
        # 'javascript error: document unloaded while waiting for result'
        for _ in range(5):  # 5 attempts max
            try:
                result = self.browser.driver.execute_async_script(dedent(javascript))
            except WebDriverException as wde:
                if "document unloaded while waiting for result" in wde.msg:
                    # Wait a bit, and try again, when the browser has reloaded the page.
                    time.sleep(1)
                    continue
                else:
                    raise
            return result

    def trigger_event(self, css_selector, event='change', index=0):
        self.browser.execute_script("$('{}:eq({})').trigger('{}')".format(css_selector, index, event))

    def disable_jquery_animations(self):
        """
        Disable JQuery animations on the page.  Any state changes
        will occur immediately to the final state.
        """

        # Ensure that jquery is loaded
        self.wait_for_requirejs(["jquery"])

        # Disable jQuery animations
        self.browser.execute_script("jQuery.fx.off = true;")
