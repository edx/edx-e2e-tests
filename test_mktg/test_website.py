"""
E2E tests for the Website.
"""


from bok_choy.web_app_test import WebAppTest
from pages.mktg.about_us import AboutUsPage
from pages.mktg.bios import BiosPage
from pages.mktg.contact import ContactPage
from pages.mktg.course_list import CourseListPage
from pages.mktg.edx_blog import EdxBlogPage
from pages.mktg.edx_privacy_policy import PrivacyPolicyPage
from pages.mktg.edx_terms_service import TermsOfServicePage
from pages.mktg.home_page import HomePage
from pages.mktg.how_it_works import HowItWorksPage
from pages.mktg.jobs import JobsPage
from pages.mktg.news import NewsPage
from pages.mktg.org_faq import OrgFaqPage
from pages.mktg.research_pedagogy import ResearchPedagogyPage
from pages.mktg.schools import SchoolsPage
from pages.mktg.student_faq import StudentFaqPage
from pages.mktg.verified_certificate import VerifiedCertificatePage
from pages.mktg.xseries import XSeriesPage


class WebsiteTest(WebAppTest):
    """
    Smoke test for accessing all website tests.
    """

    @property
    def page_object_classes(self):
        # Page URLS for the website are documented at:
        # https://edx-wiki.atlassian.net/wiki/display/PROD/Report%3A+URL+Alias+List
        return [
            AboutUsPage, BiosPage, ContactPage, CourseListPage,
            EdxBlogPage, PrivacyPolicyPage, TermsOfServicePage,
            HomePage, HowItWorksPage, JobsPage, NewsPage,
            OrgFaqPage, ResearchPedagogyPage, SchoolsPage, StudentFaqPage,
            VerifiedCertificatePage, XSeriesPage
        ]

    def test_page_existence(self):
        """
        Make sure that all the pages are accessible.
        Rather than fire up the browser just to check each url,
        do them all sequentially in this testcase.
        """
        pages = [
            'about_us', 'bios', 'contact', 'course_list',
            'edx_blog','edx_privacy_policy', 'edx_terms_service',
            'home_page', 'how_it_works', 'jobs', 'news', 'org_faq',
            'research_pedagogy', 'schools', 'student_faq',
            'verified_certificate', 'xseries'
        ]

        for page in pages:
            self.ui.visit('mktg.{0}'.format(page))
