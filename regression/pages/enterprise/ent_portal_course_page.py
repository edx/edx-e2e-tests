"""
Enterprise portal course start page
"""
from bok_choy.page_object import PageObject


class EntPortalCourse(PageObject):
    """
    This class handles the Enterprise Portal Course objects
    """

    IFRAME_CSS = 'iframe[name="iframelearning"]'

    url = None

    def is_browser_on_page(self):
        """
        Verifies if the browser is on the correct page
        """
        return self.q(css='iframe').visible

    def switch_to_iframe(self):
        """
        Switch to iframe
        """
        self.wait_for_element_visibility(self.IFRAME_CSS, 'wait for iframe')
        iframe = self.q(css=self.IFRAME_CSS).results[0]
        self.browser.switch_to_frame(iframe)


class EntPortalCourseStart(EntPortalCourse):
    """
    This class handles the Enterprise portal course start/continue objects
    """
    def start_or_continue_course(self):
        """
        Click on start/continue course button
        """
        self.switch_to_iframe()
        button_css = 'button[title*="Course"]'
        self.wait_for_element_visibility(button_css, 'wait for button')
        self.q(css=button_css).click()
        self.wait_for_ajax()


class EntPortalCourseStructure(EntPortalCourse):
    """
    This class handles the Enterprise portal course structure objects
    """

    def open_course_on_edx(self):
        """
        Open the edx course page in new browser window
        """
        course_link_css = '.BodyText>a'
        self.wait_for_element_visibility(course_link_css, 'wait for link')
        self.q(css=course_link_css).click()
