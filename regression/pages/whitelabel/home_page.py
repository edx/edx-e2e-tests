"""
LMS Home page
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH


class HomePage(PageObject):
    """
    LMS Home Page
    """
    url = URL_WITH_AUTH

    def is_browser_on_page(self):
        return self.q(css='.brand-link[href="/login"]').visible

    def click_registration_button(self):
        """
        Clicks registration button.
        """
        registration_button_css = '.btn-brand.btn-client[href="/register"]'
        self.wait_for_element_visibility(
            registration_button_css,
            'Registration button is visible'
        )
        self.q(css=registration_button_css).click()

    def click_login_button(self):
        """
        Clicks login button.
        """
        login_button_css = '.brand-link[href="/login"]'
        self.wait_for_element_visibility(
            login_button_css,
            'Login button is visible'
        )
        self.q(css=login_button_css).click()
