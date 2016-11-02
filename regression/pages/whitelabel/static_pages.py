"""
Marketing pages
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH


class AboutPage(PageObject):
    """
    About page
    """

    url = URL_WITH_AUTH + 'about'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if tab is active:
        """
        return 'About' in self.q(css='.page-heading>h1').text[0]


class FaqPage(PageObject):
    """
    FAQ page
    """

    url = URL_WITH_AUTH + 'faq'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if tab is active:
        """
        return 'General FAQs' in self.q(css='.page-heading>h1').text[0]


class ContactUsPage(PageObject):
    """
    Contact Us page
    """

    url = URL_WITH_AUTH + 'contact'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if tab is active:
        """
        return 'Contact Us' in self.q(css='.page-heading>h1').text[0]


class TosPage(PageObject):
    """
    TOS page
    """

    url = URL_WITH_AUTH + 'tos'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if tab is active
        """
        return 'Terms of Service' in self.q(css='.page-heading>h1').text[0]


class PrivacyPolicyPage(PageObject):
    """
    Privacy Policy Page
    """

    url = URL_WITH_AUTH + 'privacy'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if tab is active
        """
        return 'Privacy Policy' in self.q(css='.page-heading>h1').text[0]


class HonorCodePage(PageObject):
    """
    Honor Code page
    """

    url = URL_WITH_AUTH + 'honor'

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if tab is active:
        """
        return 'Honor Code' in self.q(css='.page-heading>h1').text[0]
