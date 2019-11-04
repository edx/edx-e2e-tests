"""
Grading Page for Studio
"""

from __future__ import absolute_import

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

    def is_browser_on_page(self):
        return all(
            [self.q(css='body.grading').visible,
             self.q(css=".grade-specific-bar").visible]
        )
