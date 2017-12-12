from bok_choy.page_object import PageObject, unguarded
from bok_choy.promise import Promise, EmptyPromise, BrokenPromise



class NewPageObject(PageObject):


    @unguarded
    def wait_for_page(self, timeout=30):
        """
        Block until the page loads, then returns the page.
        Useful for ensuring that we navigate successfully to a particular page.

        Keyword Args:
            timeout (int): The number of seconds to wait for the page before timing out with an exception.

        Raises:
            BrokenPromise: The timeout is exceeded without the page loading successfully.
        """

        def _is_document_interactive():
            """
            Check the loading state of the document to ensure the document is
            in interactive mode
            """
            return self.browser.execute_script(
                "return document.readyState=='interactive'")


        def _is_document_ready():
            """
            Check the loading state of the document to ensure the document and all sub-resources
            have finished loading (the document load event has been fired.)
            """
            return self.browser.execute_script(
                "return document.readyState=='complete'")

        # Wait for page to laod completely i.e. for document.readyState to
        # become complete

        try:
            EmptyPromise(
                _is_document_ready,
                "The document and all sub-resources have finished loading.",
                timeout=timeout
            ).fulfill()
        except BrokenPromise:

            # If document.readyState does not become complete after a specific
            # time relax the condition and check for the state to become
            # interactive
            EmptyPromise(
                _is_document_interactive,
                "The document is in interactive mode.",
                timeout=timeout
            ).fulfill()

        result = Promise(
            lambda: (self.is_browser_on_page(), self), "loaded page {!r}".format(self),
            timeout=timeout
        ).fulfill()

        if self.verify_accessibility:
            self.a11y_audit.check_for_accessibility_errors()  # pylint: disable=no-member

        return result