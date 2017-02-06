"""
Grading Page for Studio
"""

from edxapp_acceptance.pages.studio.settings_graders import GradingPage
from regression.tests.helpers.utils import get_url


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
