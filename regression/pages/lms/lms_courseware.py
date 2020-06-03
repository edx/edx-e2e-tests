"""
Courseware page LMS
"""
from __future__ import absolute_import

from edxapp_acceptance.pages.lms.courseware import CoursewarePage
from regression.pages.lms import LOGIN_BASE_URL


class CoursewarePageExtended(CoursewarePage):
    """
    This class is an extended class of Courseware Page,
    where we add methods that are different or not used in
    Courseware Page
    """

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return LOGIN_BASE_URL + "/courses/" + self.course_id + "/courseware"

    def submit_graded_problem(self):
        """
        Submits graded problem
        """
        self.q(css='input[value="choice_1"]').first.click()
        self.q(css='.problem .submit').first.click()
        self.wait_for_element_visibility('.notification.success', 'wait for problem submission notification')

    def view_unit_in_studio(self):
        """
        Clicks on the 'View unit in Studio' button
        """
        self.q(css='.preview-menu .view-in-studio').click()

    def go_to_section(self, section_title, subsection_title):
        """
        Go to the section in the courseware.
        Every section must have at least one subsection, so specify
        both the section and subsection title.

        Example:
            go_to_section("Week 1", "Lesson 1")
        """

        # Get the section by index
        try:
            section_index = self._section_titles().index(section_title)
        except ValueError:
            self.warning("Could not find section '{0}'".format(section_title))
            return

        # Get the subsection by index
        try:
            subsection_index = self._subsection_titles(
                section_index + 1
            ).index(subsection_title)
        except ValueError:
            msg = "Could not find subsection '{0}' in section '{1}'".format(
                subsection_title, section_title
            )
            self.warning(msg)
            return

        # Convert list indices (start at zero) to CSS indices (start at 1)
        subsection_css = (
            ".outline-item.section:nth-of-type({0}) "
            ".subsection:nth-of-type({1}) .outline-item"
        ).format(section_index + 1, subsection_index + 1)

        # Click the subsection and ensure that the page finishes reloading
        self.q(css=subsection_css).first.click()
        self.courseware_page.wait_for_page()
        self._wait_for_course_section(section_title, subsection_title)

    def _section_titles(self):
        """
        Return a list of all section titles on the page.
        """
        section_css = '.section-name span'
        return self.q(css=section_css).map(lambda el: el.text.strip()).results

    def _subsection_titles(self, section_index):
        """
        Return a list of all subsection titles on the page
        for the section at index `section_index` (starts at 1).
        """
        # Retrieve the subsection title for the section
        # Add one to the list index to get the CSS index, which starts at one
        subsection_css = (
            ".outline-item.section:nth-of-type({0}) .subsection a"
        ).format(section_index)

        return self.q(
            css=subsection_css
        ).map(
            lambda el: el.get_attribute('innerHTML').strip()
        ).results

    def _wait_for_course_section(self, section_title, subsection_title):
        """
        Ensures the user navigates to the course content page with the correct
        section and subsection.
        """
        self.wait_for(
            promise_check_func=lambda: self.courseware_page.nav.is_on_section(
                section_title, subsection_title
            ),
            description="Waiting for course page with section '{0}' and "
                        "subsection '{1}'".format(
                            section_title, subsection_title)
        )

    def get_page_names_in_tab(self):
        """
        Get names of all pages in tab

        Returns
            list: A list of names of all pages
        """
        tab_pages = self.q(css='.tabs.course-tabs .tab').text
        # There is an extra text 'Current location' along
        # the page's name of selected(active) tab. It is
        # not required, so removing it.
        return [page.replace('\n, current location', "") for page in tab_pages]
