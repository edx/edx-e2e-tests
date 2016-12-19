"""
Drupal course page.
"""
from bok_choy.page_object import PageObject
from regression.pages.lms import BASE_URL_LMS


class DemoCourseSelectionPage(PageObject):
    """
    Drupal demo course page
    """
    @property
    def url(self):
        """
        Construct a URL to the page
        This URL is different from the base url and it won't be used
        anywhere else so we have to make it like this to hit Drupal
        """
        # This is the test course we are using for this test
        # This course/page won't be used for any tests
        course_to_enroll = 'demox-edx-demox-1'

        return BASE_URL_LMS + "/course/" + course_to_enroll

    def is_browser_on_page(self):
        """
        Checks if we are on the correct page
        """
        return 'DemoX' in self.q(
            css='.pull-left'
        ).text[0]

    def click_enroll_now(self):
        """
        Clicks Enroll Now button
        """
        self.q(css='.js-enroll-btn').click()
