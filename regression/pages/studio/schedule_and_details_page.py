"""
Course Schedule and Details Page for Studio
"""
from bok_choy.page_object import PageObject
from regression.pages.studio import BASE_URL


class StudioScheduleDetails(PageObject):
    """
    Course Schedule and Details Page for Studio
    """

    url = BASE_URL

    def is_browser_on_page(self):
        """
        Checks if we are on the correct page
        """
        return self.q(css='#upload-course-image').visible
