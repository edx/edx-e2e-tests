from e2e_framework.page_object import PageObject
from ..lms import BASE_URL


class LoginPage(PageObject):
    """
    Login page for the LMS.
    """

    @property
    def name(self):
        return "lms.login"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + "/login"

    def is_browser_on_page(self):
        return any([
            'log in' in title.lower()
            for title in self.css_text('span.title-super')
        ])

    def login(self, email, password):
        """
        Attempt to log in using `email` and `password`.
        """
        self.css_fill('input#email', email)
        self.css_fill('input#password', password)
        self.css_click('button#submit')
