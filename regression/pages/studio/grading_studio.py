"""
Grading Page for Studio
"""
import urllib

from edxapp_acceptance.pages.studio.settings_graders import GradingPage

from regression.pages.studio.utils import press_the_notification_button
from regression.pages.studio.utils import get_course_key
from regression.pages.studio import BASE_URL


class GradingPageExtended(GradingPage):
    """
    Grading Page for Studio
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        course_key = get_course_key(self.course_info)
        url = "/".join(
            [BASE_URL, self.url_path, urllib.quote_plus(unicode(course_key))])
        return url if url[-1] is '/' else url + '/'

    def letter_grade(self, selector):
        """
        Returns: first letter of grades on grading page
        """
        return self.q(css=selector)[0].text

    def click_new_grade_button(self):
        """
        Clicks new grade button
        """
        self.q(css='.new-grade-button').click()
        press_the_notification_button(self, "save")
        self.wait_for_element_visibility(
            '#alert-confirmation-title',
            'Save confirmation message is visible'
        )

    def click_remove_grade(self):
        """
        Clicks remove grade button
        """
        # Button displays after hovering on it
        btn_css = '.remove-button'
        self.browser.execute_script("$('{}').focus().click()".format(btn_css))
        self.wait_for_ajax()
        press_the_notification_button(self, "save")
        self.wait_for_element_visibility(
            '#alert-confirmation-title',
            'Save confirmation message is visible'
        )
