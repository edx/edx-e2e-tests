from e2e_framework.page_object import PageObject
from . import BASE_URL


class InfoPage(PageObject):
    """
    Info pages for the main site.
    These are basically static pages, so we use one page
    object to represent them all.
    """

    # Dictionary mapping section names to URL paths
    SECTION_PATH = {
        'about': '/about',
        'faq': '/faq',
        'press': '/press',
        'contact': '/contact',
        'terms': '/tos',
        'privacy': '/privacy',
        'honor': '/honor',
    } 

    # Dictionary mapping URLs to expected css selector 
    EXPECTED_CSS = {
        '/about': 'section.vision',
        '/faq': 'section.faq',
        '/press': 'section.press',
        '/contact': 'section.contact',
        '/tos': 'section.tos',
        '/privacy': 'section.privacy-policy',
        '/honor': 'section.honor-code',
    }

    @property
    def name(self):
        return "lms.info"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self, section=None):
        return BASE_URL + self.SECTION_PATH[section]

    def is_browser_on_page(self):
        stripped_url = self.browser.url.replace(BASE_URL, "")
        css_sel = self.EXPECTED_CSS[stripped_url]
        return self.is_css_present(css_sel)

    @classmethod
    def sections(cls):
        return cls.SECTION_PATH.keys()
