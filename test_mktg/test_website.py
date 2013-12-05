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
from pages.mktg.media_kit import MediaKitPage
from pages.mktg.news import NewsPage
from pages.mktg.org_faq import OrgFaqPage
from pages.mktg.press_releases import PressReleasesPage
from pages.mktg.research_pedagogy import ResearchPedagogyPage
from pages.mktg.schools import SchoolsPage
from pages.mktg.student_faq import StudentFaqPage
from pages.mktg.verified_certificate import VerifiedCertificatePage
from pages.mktg.xseries import XSeriesPage

from nose.tools import assert_equal, assert_not_equal
from nose.plugins.skip import SkipTest


class WebsitePageTest(WebAppTest):
    """
    Smoke test for accessing all website pages.
    """

    @property
    def page_object_classes(self):
        # Page URLS for the website are documented at:
        # https://edx-wiki.atlassian.net/wiki/display/PROD/Report%3A+URL+Alias+List
        return [
            AboutUsPage, BiosPage, ContactPage, CourseListPage,
            EdxBlogPage, PrivacyPolicyPage, TermsOfServicePage,
            HomePage, HowItWorksPage, JobsPage, MediaKitPage, NewsPage, OrgFaqPage,
            PressReleasesPage, ResearchPedagogyPage, SchoolsPage, StudentFaqPage,
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
            'home_page', 'how_it_works', 'jobs', 'media_kit', 'news', 'org_faq',
            'press_releases', 'research_pedagogy', 'schools', 'student_faq',
            'verified_certificate', 'xseries'
        ]

        for page in pages:
            self.ui.visit('mktg.{0}'.format(page))


class FindCoursesTest(WebAppTest):
    """
    Smoke test for course filtering
    """
    @property
    def page_object_classes(self):
        return [
            CourseListPage
        ]

    def test_pagination_at_15(self):
        # Visit the main page with the list of courses
        # Note that this will default to showing all courses.
        self.ui.visit('mktg.course_list')

        # Grab the courses shown and total count
        displayed = self.ui['mktg.course_list'].results_displayed

        # By default we should only show the first 15 results
        assert_equal(displayed['start'], 1)

        # There should be more than 15 courses in most environments,
        # but if there isn't, make sure that you show all of them.
        if (displayed['total'] > 15):
            assert_equal(displayed['end'], 15)
        else:
            assert_equal(displayed['end'], displayed['total'])


    def test_pagination_next(self):
        # Visit the main page with the list of courses
        # Note that this will default to showing all courses.
        self.ui.visit('mktg.course_list')

        # Grab the courses shown and total count
        orig_num = self.ui['mktg.course_list'].results_displayed
        # Grab the titles of the courses being displayed
        orig_titles = self.ui['mktg.course_list'].course_titles

        # There should be more than 15 courses in most environments,
        # if there isn't this test would not be applicable
        if (orig_num['total'] < 16):
            msg = 'Skipping pagination test because there are not enough courses'
            raise SkipTest(msg)

        # press the next link
        self.ui['mktg.course_list'].show_results('next')

        # Verify that the results have incremented
        new_num = self.ui['mktg.course_list'].results_displayed
        assert_equal(new_num['start'], orig_num['start']+15)

        # Verify that the courses displayed have changed
        new_titles = self.ui['mktg.course_list'].course_titles
        assert_not_equal(new_titles, orig_titles)


    def test_pagination_last(self):
        # Visit the main page with the list of courses
        # Note that this will default to showing all courses.
        self.ui.visit('mktg.course_list')

        # Grab the courses shown and total count
        orig_num = self.ui['mktg.course_list'].results_displayed
        # Grab the titles of the courses being displayed
        orig_titles = self.ui['mktg.course_list'].course_titles

        # There should be more than 15 courses in most environments,
        # if there isn't this test would not be applicable
        if (orig_num['total'] < 16):
            msg = 'Skipping pagination test because there are not enough courses'
            raise SkipTest(msg)

        # press the next link
        self.ui['mktg.course_list'].show_results('last')

        # Verify that the results have incremented
        new_num = self.ui['mktg.course_list'].results_displayed
        assert_equal(new_num['end'], orig_num['total'])

        # Verify that the courses displayed have changed
        new_titles = self.ui['mktg.course_list'].course_titles
        assert_not_equal(new_titles, orig_titles)
