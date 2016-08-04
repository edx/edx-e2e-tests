"""
Grading Page for Studio
"""

from edxapp_acceptance.pages.studio.settings_graders import GradingPage

from edxapp_acceptance.pages.studio.utils import press_the_notification_button
from regression.tests.helpers import get_url


class GradingPageExtended(GradingPage):
    """
    Grading Page for Studio
    """
    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return get_url(self.url_path, self.course_info)

    def letter_grade(self, selector):
        """
        Returns: first letter of grade range on grading page
        Example: if there are no manually added grades it would
        return Pass, if a grade is added it will return 'A'
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
