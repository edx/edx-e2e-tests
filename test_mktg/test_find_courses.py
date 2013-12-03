"""
End to end tests for finding courses
"""
from bok_choy.web_app_test import WebAppTest
from pages.mktg.course_list import CourseListPage
from nose.tools import assert_equal, assert_not_equal
from nose.plugins.skip import SkipTest


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

