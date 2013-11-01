from e2e_framework.page_object import PageObject
from ..mktg import BASE_URL
import re

class ParseError(Exception):
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
    def num_results_shown(self):
        """
        Return a dict of the number of results displayed on the
        screen as parsed from the text shown.
        Keys are: start, end, total
        Values are of type int.

        Example: "Courses: Showing 1 - 15 of 86" yields:
        {'start': 1, 'total': 86, 'end': 15}
        """
        # Get the text noting the courses shown.
        text = self.css_text('div.view-header')[0]

        parsed = re.match('^Courses:\s*Showing (\d+) - (\d+) of (\d+)\s*$', text)
        if (parsed is not None) and (len(parsed.groups()) == 3):

            return dict(zip(['start', 'end', 'total'], map(int, parsed.groups())))

        else:
            msg = 'Cannot parse the results displayed from the string: {0}'.format(
                text
            )
            raise ParseError(msg)

    @property
    def course_title_list(self):
        """
        Retrieve the list of available course IDs on the page.
        """
        return self.css_text('h2.course-title')

    def press_pager_link(self, text):
        """
        Press the pager link to display different courses in the list.
        For the text, use either the number of the page, or one of
        these words: first, previous, next, last
        """
        if text in ['first', 'previous', 'next', 'last']:
            title = 'Go to {0} page'.format(text)
        else:
            title = 'Go to page {0}'.format(text)

        self.css_click('a[title="{0}"]'.format(title))
