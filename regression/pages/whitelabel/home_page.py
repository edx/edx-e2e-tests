"""
Home page for LMS
"""
from bok_choy.page_object import PageObject

from regression.pages.whitelabel.const import URL_WITH_AUTH
from regression.pages.whitelabel.course_about_page import CourseAboutPage
from regression.pages.whitelabel.courses_page import CoursesPage
from regression.pages.whitelabel.logistration_page import (
    LoginPage,
    RegistrationPage
)


class HomePage(PageObject):
    """
    Home page
    """

    # Open White label site in browser#
    url = URL_WITH_AUTH

    def is_browser_on_page(self):
        """
        Is browser on the page?
        Returns:
            True if login button is visible on the page:
        """
        return self.q(css='.brand-link[href="/login"]').visible

    @property
    def social_links(self):
        """
        Get list of social media links
        Returns:
            social media links:
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
            header logo link:
        """
        return self.q(css='.logo>a>img').attrs('src')[0]

    @property
    def header_logo_alt_text(self):
        """
        Get header logo alt text
        Returns:
            header logo alt text:
        """
        return self.q(css='.logo>a>img').attrs('alt')[0]

    @property
    def footer_logo_link(self):
        """
        Get footer logo link
        Returns:
            footer logo link:
        """
        return self.q(css='.footer-logo>ul>li>a>img').attrs('src')[0]

    @property
    def footer_logo_alt_text(self):
        """
        Get footer logo alt text
        Returns:
            footer logo alt text:
        """
        return self.q(css='.footer-logo>ul>li>a>img').attrs('alt')[0]

    def go_to_login_page(self):
        """
        click on the login button
        """
        self.q(css='.brand-link[href="/login"]').click()
        LoginPage(self.browser).wait_for_page()

    def go_to_course_about_page(self, course_id):
        """
        Click on the desired course id to go to course about page
        Args:
            course_id:

        """
        self.q(css='article[id="' + course_id + '"]>a').click()
        CourseAboutPage(self.browser, course_id).wait_for_page()

    def go_to_courses_page(self):
        """
        Go to courses page
        """
        self.q(css='.brand-link[href="/courses"]').click()
        CoursesPage(self.browser).wait_for_page()

    def go_to_registration_page(self):
        """
        Go to registration page
        """
        self.q(css='.btn-brand.btn-client[href="/register"]').click()
        RegistrationPage(self.browser).wait_for_page()
