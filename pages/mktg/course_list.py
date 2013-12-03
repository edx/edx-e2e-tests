from bok_choy.page_object import PageObject
from bok_choy.promise import EmptyPromise, fulfill_after
from ..mktg import BASE_URL
import re

class CourseListPageError(Exception):
    """
    Could not parsing the number of results displayed
    on the course list page.
    """
    pass


class CourseListPage(PageObject):
    """
    The page on the website for finding courses
    """

    @property
    def name(self):
        return 'mktg.course_list'

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self):
        return BASE_URL + '/course-list'

    def is_browser_on_page(self):
        return self.is_css_present('div.page-courses-all')

    @property
    def results_displayed(self):
        """
        Return a dict of the number of results displayed on the
        screen as parsed from the text shown.
        Keys are: start, end, total
        Values are of type int.

        If no courses are displayed (e.g. the filter is set such that
        no courses meet the criteria) then return None

        Example: "Courses: Showing 1 - 15 of 86" yields:
        {'start': 1, 'total': 86, 'end': 15}
        """
        # Get the text noting the courses shown.
        results_text_css = 'div.view-header'
        if self.css_count('div.view-header') == 0:
            self.warning('No courses are currently displayed.')
            return None

        text = self.css_text(results_text_css)[0]
        parsed = re.match('^Courses:\s*Showing (\d+) - (\d+) of (\d+)\s*$', text)

        if (parsed is not None) and (len(parsed.groups()) == 3):
            return dict(zip(['start', 'end', 'total'], map(int, parsed.groups())))

        else:
            msg = 'Cannot parse the results displayed from the string: {0}'.format(
                text
            )
            raise CourseListPageError(msg)

    @property
    def course_titles(self):
        """
        Retrieve the list of available course IDs on the page.
        """
        return self.css_text('h2.course-title')

    def show_results(self, text):
        """
        Press the pager link to display different courses in the list.
        For the text, use either the number of the page, or one of
        these words: first, previous, next, last
        """
        if text in ['first', 'previous', 'next', 'last']:
            title = 'Go to {0} page'.format(text)
        else:
            title = 'Go to page {0}'.format(text)

        pagination_promise = EmptyPromise(
            lambda: self.is_browser_on_page,
            'redrew the page'
        )
        with fulfill_after(pagination_promise):
            self.css_click('a[title="{0}"]'.format(title))
