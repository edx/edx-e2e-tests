"""
End to end tests for finding courses
"""
from e2e_framework.web_app_test import WebAppTest
from pages.mktg.course_list import CourseListPage
from nose.tools import assert_equal, assert_not_equal


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
        displayed = self.ui['mktg.course_list'].num_results_shown

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
        orig_num = self.ui['mktg.course_list'].num_results_shown
        # Grab the titles of the courses being displayed
        orig_titles = self.ui['mktg.course_list'].course_title_list

        # There should be more than 15 courses in most environments,
        # if there isn't this test would not be applicable
        if (orig_num['total'] < 16):
            pass

        # press the next link
        self.ui['mktg.course_list'].press_pager_link('next')

        # Verify that the results have incremented
        new_num = self.ui['mktg.course_list'].num_results_shown
        assert_equal(new_num['start'], orig_num['start']+15)

        # Verify that the courses displayed have changed
        new_titles = self.ui['mktg.course_list'].course_title_list
        assert_not_equal(new_titles, orig_titles)


    def test_pagination_last(self):
        # Visit the main page with the list of courses
        # Note that this will default to showing all courses.
        self.ui.visit('mktg.course_list')

        # Grab the courses shown and total count
        orig_num = self.ui['mktg.course_list'].num_results_shown
        # Grab the titles of the courses being displayed
        orig_titles = self.ui['mktg.course_list'].course_title_list

        # There should be more than 15 courses in most environments,
        # if there isn't this test would not be applicable
        if (orig_num['total'] < 16):
            pass

        # press the next link
        self.ui['mktg.course_list'].press_pager_link('last')

        # Verify that the results have incremented
        new_num = self.ui['mktg.course_list'].num_results_shown
        assert_equal(new_num['end'], orig_num['total'])

        # Verify that the courses displayed have changed
        new_titles = self.ui['mktg.course_list'].course_title_list
        assert_not_equal(new_titles, orig_titles)

