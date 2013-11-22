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
        tab_css = 'ol.course-tabs li a'
        tabs = [el for el in self.css_find(tab_css) if tab_name.lower() in el.text.lower()]

        if len(tabs) > 1:
            self.warning("Multiple tabs found for '{0}'.  Clicking the first one.".format(tab_name))
            tabs[0].click()

        elif len(tabs) < 1:
            self.warning("No tabs found for '{0}'".format(tab_name))

        else:
            tabs[0].click()
