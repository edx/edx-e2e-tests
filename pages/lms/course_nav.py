from e2e_framework.page_object import PageObject
from pages import BASE_URL


class CourseNavPage(PageObject):
    """
    Navigate sections and sequences in the courseware.
    """

    @property
    def name(self):
        return "lms.course_nav"

    @property
    def requirejs(self):
        return []

    @property
    def js_globals(self):
        return []

    def url(self, **kwargs):
        """
        Since course navigation appears on multiple pages,
        it doesn't have a particular URL.
        """
        raise NotImplemented

    def is_browser_on_page(self):
        return self.is_css_present('section.course-index')

    @property
    def sections(self):
        """
        Return a dictionary representation of sections and subsections.

        Example:

            {
                'Introduction': ['Course Overview'],
                'Week 1': ['Lesson 1', 'Lesson 2', 'Homework']
                'Final Exam': ['Final Exam']
            }

        You can use these titles in `go_to_section` to navigate to the section.
        """
        # Dict to store the result
        nav_dict = dict()

        section_titles = self._section_titles()

        # Get the section titles for each chapter
        for sec_index in range(len(section_titles)):

            sec_title = section_titles[sec_index]

            if len(section_titles) < 1:
                self.warning("Could not find subsections for '{0}'".format(sec_title))
            else:
                # Add one to convert list index (starts at 0) to CSS index (starts at 1)
                nav_dict[sec_title] = self._subsection_titles(sec_index + 1)

        return nav_dict

    @property
    def sequence_items(self):
        """
        Return a list of sequence items on the page.
        Sequence items are one level below subsections in the course nav.

        Example return value:
            ['Chemical Bonds Video', 'Practice Problems', 'Homework']
        """
        seq_css = 'ol#sequence-list>li>a>p'
        seq_titles = [el.html.strip() for el in self.css_find(seq_css)]

        # Need to strip out the span tag text after the first line
        return [title.split('\n')[0] for title in seq_titles]

    def go_to_section(self, section_title, subsection_title):
        """
        Go to the section in the courseware.
        Every section must have at least one subsection, so specify
        both the section and subsection title.

        Example:
            go_to_section("Week 1", "Lesson 1")
        """

        # For test stability, disable JQuery animations (opening / closing menus)
        self.disable_jquery_animations()

        # Get the section by index
        try:
            sec_index = self._section_titles().index(section_title)
        except ValueError:
            self.warning("Could not find section '{0}'".format(section_title))
            return

        # Click the section to ensure it's open (no harm in clicking twice if it's already open)
        # Add one to convert from list index to CSS index
        section_css = 'nav>div.chapter:nth-of-type({0})>h3>a'.format(sec_index + 1)
        self.css_click(section_css)

        # Get the subsection by index
        try:
            subsec_index = self._subsection_titles(sec_index + 1).index(subsection_title)
        except ValueError:
            msg = "Could not find subsection '{0}' in section '{1}'".format(subsection_title, section_title)
            self.warning(msg)
            return

        # Click the subsection
        # Convert list indices (start at zero) to CSS indices (start at 1)
        subsection_css = "nav>div.chapter:nth-of-type({0})>ul>li:nth-of-type({1})>a".format(
            sec_index + 1, subsec_index + 1
        )
        self.css_click(subsection_css)

    def go_to_sequential(self, sequential_title):
        """
        Within a section/subsection, navigate to the sequential with `sequential_title`.
        If the same title occurs multiple times, go to the first one.
        """

        # Get the index of the item in the sequence
        all_items = self.sequence_items

        try:
            # This will return the first item that matches the title
            seq_index = all_items.index(sequential_title)

        except ValueError:
            msg = "Could not find sequential '{0}'.  Available sequentials: [{1}]".format(
                sequential_title, ", ".join(all_items)
            )
            self.warning(msg)

        else:

            # Click on the sequence item at the correct index
            # Convert the list index (starts at 0) to a CSS index (starts at 1)
            seq_css = "ol#sequence-list>li:nth-of-type({0})>a".format(seq_index + 1)
            self.css_click(seq_css)

    def _section_titles(self):
        """
        Return a list of all section titles on the page.
        """
        chapter_css = 'nav>div.chapter>h3>a'
        return [el.text.strip() for el in self.css_find(chapter_css)]

    def _subsection_titles(self, section_index):
        """
        Return a list of all subsection titles on the page
        for the section at index `section_index` (starts at 1).
        """
        # Retrieve the subsection title for the section
        # Add one to the list index to get the CSS index, which starts at one
        subsection_css = 'nav>div.chapter:nth-of-type({0})>ul>li>a>p:nth-of-type(1)'.format(section_index)

        # If the element is visible, we can get its text directly
        # Otherwise, we need to get the HTML
        # It *would* make sense to always get the HTML, but unfortunately
        # the open tab has some child <span> tags that we don't want.
        subsection_titles = [
            el.text.strip() if el.visible else el.html.strip()
            for el in self.css_find(subsection_css)
        ]

        # Section title text sometimes picks up trailing text on the next line
        # So include only the first line
        return [title.split('\n')[0] for title in subsection_titles]
