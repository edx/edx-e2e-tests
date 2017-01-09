"""
Dashboard page for Studio
"""
from edxapp_acceptance.pages.studio.index import DashboardPage
from bok_choy.promise import BrokenPromise
from regression.pages.studio import BASE_URL
from regression.pages.lms import BASE_URL_LMS
from regression.tests.helpers import get_course_info
from regression.pages.lms.utils import get_course_key


class DashboardPageExtended(DashboardPage):
    """
    This class is an extended class of Studio Dashboard Page,
    where we add methods that are different or not used in DashboardPage
    """

    url = BASE_URL + '/home'
    course_details = get_course_key(get_course_info())

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
        self.q(css='.account-username').click()
        self.wait_for_element_visibility(
            '.action-signout', 'Sign out button visibility')
        self.q(css='.action-signout').click()

    def click_view_live_button(self):
        """
        Clicks view live button
        """
        self.browser.execute_script(
            "document.querySelectorAll('[data-course-key = \"{}\"] "
            ".view-button')[0].click();".format(self.course_details))
        self.browser.switch_to_window(self.browser.window_handles[-1])

    def click_terms_of_service(self):
        """
        Clicks Terms of Service link
        """
        self.q(css='a[href="' + BASE_URL_LMS + '/edx-terms-service"]').click()

    def click_privacy_policy(self):
        """
        Clicks Privacy Policy link
        """
        self.q(
            css='a[href="' + BASE_URL_LMS + '/edx-privacy-policy"]').click()

    def click_course_rerun(self):
        """
        Clicks rerun course button
        """
        self.browser.execute_script(
            "document.querySelectorAll('[data-course-key = \"{}\"] "
            ".rerun-button')[0].click();".format(self.course_details))
