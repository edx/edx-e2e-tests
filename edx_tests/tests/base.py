"""
Base class for testing a web application.
"""

from unittest import TestCase
from abc import ABCMeta, abstractproperty, abstractmethod
import os.path
from uuid import uuid4

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


class TestCredentials(object):
    """
    Encapsulate fake user information.
    """

    BASE_EMAIL_USER = "will"
    EMAIL_DOMAIN = "edx.org"

    def __init__(self):
        """
        Initialize new credentials.
        """

        unique_id = str(uuid4())[0:8]

        self._username = "{0}_{1}".format(
            self.BASE_EMAIL_USER, unique_id
        )

        self._email = "{0}+{1}@{2}".format(
            self.BASE_EMAIL_USER, unique_id, self.EMAIL_DOMAIN
        )

        self._full_name = "{0} {1}".format(
            self.BASE_EMAIL_USER, unique_id
        )

        self._password = unique_id

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def full_name(self):
        return self._full_name

    @property
    def password(self):
        return self._password
