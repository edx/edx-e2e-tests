from e2e_framework.page_object import PageObject
from ..lms import BASE_URL


class TabNavPage(PageObject):
    """
    High-level tab navigation.
    """

    @property
    def name(self):
        return "lms.tab_nav"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self, **kwargs):
        """
        Since tab navigation appears on multiple pages,
        it doesn't have a particular URL.
        """
        raise NotImplemented

    def is_browser_on_page(self):
        return self.is_css_present('ol.course-tabs')

    def go_to_tab(self, tab_name):
        """
        Navigate to the tab `tab_name`.
        """
        if tab_name not in ['Courseware', 'Course Info', 'Discussion', 'Wiki', 'Progress']:
            self.warning("'{0}' is not a valid tab name".format(tab_name))

        # The only identifier for individual tabs is the link href
        # so we find the tab with `tab_name` in its text.
        tab_css = self._tab_css(tab_name)

        if tab_css is not None:
            self.css_click(tab_css)
        else:
            self.warning("No tabs found for '{0}'".format(tab_name))

    def _tab_css(self, tab_name):
        """
        Return the CSS to click for `tab_name`.
        """
        all_tabs = self.css_text('ol.course-tabs li a')

        try:
            tab_index = all_tabs.index(tab_name)
        except ValueError:
            return None
        else:
            return 'ol.course-tabs li:nth-of-type({0}) a'.format(tab_index + 1)
