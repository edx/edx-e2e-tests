"""
Base class for testing a web application.
"""
from unittest import TestCase
from abc import ABCMeta, abstractproperty
from e2e_framework.web_app_ui import WebAppUI


class WebAppTest(TestCase):
    """
    Base class for testing a web application.
    """

    __metaclass__ = ABCMeta

    # Execute tests in parallel!
    _multiprocess_can_split_ = True

    # Subclasses can use this property
    # to access the `WebAppUI` object under test
    ui = None

    def setUp(self):
        # If using SauceLabs, tag the job with test info
        tags = [self.id()]

        # Set up the page objects
        # This will start the browser, so add a cleanup
        self.ui = WebAppUI(self.page_object_classes, tags)
        self.addCleanup(self.ui.quit_browser)

    @abstractproperty
    def page_object_classes(self):
        """
        Subclasses override this to return a list
        of `PageObject` subclasses to visit
        during the test.
        """
        return []
