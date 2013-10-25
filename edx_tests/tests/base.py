"""
Base class for testing a web application.
"""

from unittest import TestCase
from abc import ABCMeta, abstractproperty, abstractmethod
import os.path

from e2e_framework.WebAppUI import WebAppUI, WrongPageError


class WebAppTest(TestCase):
    """
    Base class for testing a web application.
    """

    __metaclass__ = ABCMeta

    # The browser to use when testing the web app
    TEST_BROWSER = "chrome"

    # Subclasses can use this property
    # to access the `WebAppUI` object under test
    ui = None

    def setUp(self):

        # Set up the page objects
        # This will start the browser, so add a cleanup
        self.ui = WebAppUI(self.TEST_BROWSER, self.page_object_classes)
        self.addCleanup(self.ui.quit_browser)

        # Delegate to concrete subclasses to set up the app
        self.setup_app()

    @abstractproperty
    def page_object_classes(self):
        """
        Subclasses override this to return a list
        of `PageObject` subclasses to visit
        during the test.
        """
        return []

    @abstractmethod
    def setup_app(self):
        """
        Perform any setup required to gain
        access to the pages under test.

        This can include:

            * Flushing databases
            * Installing fixtures
            * Creating accounts
            * Logging in

        When this method exits, all the page objects
        should be accessible.
        """
        pass
