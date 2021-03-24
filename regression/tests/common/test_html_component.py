"""
End to end tests for HTML Components
"""
import time
from uuid import uuid4

from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.lms_courseware import CoursewarePageExtended
from regression.pages.lms.utils import get_course_key
from regression.pages.studio.course_outline_page import CourseOutlinePageExtended
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.studio.unit_page import UnitPageExtended
from regression.tests.helpers.api_clients import LmsLoginApi
from regression.tests.helpers.utils import get_course_info, get_data_locator


class StudioLmsComponentBaseTest(WebAppTest):
    """
    Base class for component tests
    """
    def setUp(self):
        """
        Common setup for component tests
        """
        super().setUp()

        lms_login = LmsLoginApi()
        lms_login.authenticate(self.browser)

        self.unit_container_page = UnitPageExtended(
            self.browser, None
        )

        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePageExtended(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

        self.lms_courseware = CoursewarePageExtended(
            self.browser,
            get_course_key(self.course_info)
        )
        self.studio_course_outline.visit()
        # Delete any existing sections
        self.studio_course_outline.delete_all_sections()


class StudioViewTest(StudioLmsComponentBaseTest):
    """
    HTML Components tests related to 'studio view' of component.
    """

    def test_unit_studio_view(self):
        """
        Scenario: To test studio view of component from LMS
        Given that I am at the LMS side of the edX.
        And I open a component
        And I click on the 'View unit in Studio' button
        Then correct component should open.
        """
        section_name = f'Section :{uuid4().hex}'
        subsection_name = f'Subsection :{uuid4().hex}'
        # Add a section.
        self.studio_course_outline.add_section_with_name(section_name)
        # Add a subsection.
        self.studio_course_outline.add_subsection_with_name(subsection_name)
        # Add a unit ( In this case Word Cloud Advance component) and publish.
        self.studio_course_outline.click_add_unit_button()
        self.unit_container_page.wait_for_page()
        self.unit_container_page.add_word_cloud_component(True)
        # Get unique data locator id of the unit added).
        data_locator = get_data_locator(self.unit_container_page)
        self.lms_courseware.visit()
        self.lms_courseware.go_to_section(section_name, subsection_name)
        # View unit in the studio
        self.lms_courseware.view_unit_in_studio()
        time.sleep(5)
        assert  self.unit_container_page.url=='studio.devstack.edx:18010/container/1'
        self.unit_container_page.wait_for_page()
        # Correct unit component should open.
        self.assertEqual(
            get_data_locator(self.unit_container_page),
            data_locator, 'Correct component is opened'
        )
        # Remove the added section
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()
