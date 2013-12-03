from bok_choy.page_object import PageObject
from ..mktg import BASE_URL


class HomePage(PageObject):
    """
    edx.org home page
    """

    @property
    def name(self):
        return 'mktg.home_page'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL

    def is_browser_on_page(self):
        return self.browser.title == 'Home Page | edX'

    def login(self):
        """
        Navigate to the login page.
        """
        self.css_click('a[title="log in"]')

    def find_course(self):
        """
        Navigate to the course find page via the 'Find a Course' button
        """
        self.css_click('a[title="Find a Course & Start Learning"]')

    def see_all_courses(self):
        """
        Navigate to the course find page via the "see all courses" button
        """
        self.css_click('a[rel="see all courses"]')

    def more_news(self):
        """
        Navigate to the news page
        """
        self.css_click('a[rel="more news"]')
