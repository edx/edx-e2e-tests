"""
LMS Home page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject

from regression.pages.whitelabel import LMS_URL_WITH_AUTH


class HomePage(PageObject):
    """
    LMS Home Page
    """
    url = LMS_URL_WITH_AUTH

    def is_browser_on_page(self):
        """
        Verify that login button is visible
        """
        return self.q(css='.nav-links .sign-in-btn.btn').visible

    def click_registration_button(self):
        """
        Clicks registration button.
        """
        registration_button_css = '.nav-links .register-btn.btn'
        self.wait_for_element_visibility(
            registration_button_css,
            'Registration button is visible'
        )
        self.q(css=registration_button_css).click()

    def click_login_button(self):
        """
        Clicks login button.
        """
        login_button_css = '.nav-links .sign-in-btn.btn'
        self.wait_for_element_visibility(
            login_button_css,
            'Login button is visible'
        )
        self.q(css=login_button_css).click()

    @property
    def social_links(self):
        """
        Get list of social media links
        Returns:
            social media links
        """
        footer_css = '.footer-main a'
        social_links = []
        face_book = self.q(
            css=footer_css
        ).filter(lambda elem: elem.text == 'Facebook')
        twitter = self.q(
            css=footer_css
        ).filter(lambda elem: elem.text == 'Twitter')
        linked_in = self.q(
            css=footer_css
        ).filter(lambda elem: elem.text == 'LinkedIn')
        you_tube = self.q(
            css=footer_css
        ).filter(lambda elem: elem.text == 'YouTube')
        instagram = self.q(
            css=footer_css
        ).filter(lambda elem: elem.text == 'Instagram')
        for link in [face_book, twitter, linked_in, you_tube, instagram]:
            if link:
                social_links.append(link.attrs('href')[0])
        return social_links

    @property
    def header_logo_link(self):
        """
        Get header logo link
        Returns:
            header logo link
        """
        return self.q(css='.logo').attrs('src')[0]

    @property
    def header_logo_alt_text(self):
        """
        Get header logo alt text
        Returns:
            header logo alt text
        """
        return self.q(css='.logo').attrs('alt')[0]

    @property
    def footer_logo_link(self):
        """
        Get footer logo link
        Returns:
            footer logo link
        """
        return self.q(css='.footer-logo img').attrs('src')[0]

    @property
    def footer_logo_alt_text(self):
        """
        Get footer logo alt text
        Returns:
            footer logo alt text
        """
        return self.q(css='.footer-logo img').attrs('alt')[0]

    def go_to_registration_page(self):
        """
        Go to registration page
        """
        # Requires wait_for_page() statement in the test
        self.q(css='.register-btn.btn').click()

    def go_to_courses_page(self):
        """
        Go to courses page
        """
        # Requires wait_for_page() statement in the test
        self.q(css='.nav-links a[href="/courses"]').click()
