"""
Video upload page
"""
from __future__ import absolute_import

from regression.pages.studio.course_page_studio import CoursePageExtended


class VideoUploadPage(CoursePageExtended):
    """
    Studio video upload page.
    """

    url_path = "videos"

    def is_browser_on_page(self):
        """
        Returns whether browser is on the page.
        """
        return self.q(css='body.view-video-uploads').visible
