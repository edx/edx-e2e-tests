"""
Dashboard page for Studio
"""
from edxapp_acceptance.pages.studio.index import DashboardPage
from bok_choy.promise import BrokenPromise
from regression.pages.studio import LOGIN_BASE_URL
from regression.pages.lms import LMS_REDIRECT_URL


class DashboardPageExtended(DashboardPage):
    """
    This class is an extended class of Studio Dashboard Page,
    where we add methods that are different or not used in DashboardPage
    """

    url = LOGIN_BASE_URL + '/home'

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return self.q(css='.courses-tab.active').present

    def select_course(self, course_title):
        """
        Selects the course we want to perform tests on
        """
        course_names = self.q(css='.course-link h3')
        for vals in course_names:
            if course_title in vals.text:
                vals.click()
                return
        raise BrokenPromise('Course title not found')

    def click_logout_button(self):
        """
        Clicks username drop down than logout button
        """
        self.wait_for_element_visibility(
            '.account-username', 'Username drop down visibility'
        )
        self.q(css='.account-username').click()
        self.wait_for_element_visibility(
            '.title.is-selected', 'Sign out button visibility'
        )
        self.q(css='.action-signout').click()

    def click_view_live_button(self):
        """
        Clicks view live button
        """
        self.browser.execute_script(
            "document.querySelectorAll('[data-course-key = \"course-v1:"
            "ArbiRaees+AR-1000+fall\"] .view-button')[0].click();")
        self.browser.switch_to_window(self.browser.window_handles[-1])

    def click_terms_of_service(self):
        """
        Clicks Terms of Service link
        """
        self.q(
            css='a[href="' + LMS_REDIRECT_URL + '/edx-terms-service"]'
        ).click()

    def click_privacy_policy(self):
        """
        Clicks Privacy Policy link
        """
        self.q(
            css='a[href="' + LMS_REDIRECT_URL + '/edx-privacy-policy"]'
        ).click()
