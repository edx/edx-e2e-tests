"""
End to end tests for HTML Components
"""
from uuid import uuid4

from bok_choy.web_app_test import WebAppTest

from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.pages.studio.unit_page import UnitPageExtended
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.lms.utils import get_course_key
from regression.pages.lms.lms_courseware import CoursewarePageExtended
from regression.tests.helpers.utils import (
    get_course_info, get_data_id_of_component, get_data_locator
)

from regression.tests.helpers.api_clients import (
    StudioLoginApi,
    LmsLoginApi
)


class StudioLmsComponentBaseTest(WebAppTest):
    """
    Base class for component tests
    """
    def setUp(self):
        """
        Common setup for component tests
        """
        super(StudioLmsComponentBaseTest, self).setUp()

        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)

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


class StudioLmsAdvancedComponentTest(StudioLmsComponentBaseTest):
    """
    Advanced Components tests that require lms verification with studio
    """
    def setUp(self):
        """
        Call setUp in parent
        """
        super(StudioLmsAdvancedComponentTest, self).setUp()

    def test_word_cloud_advanced_component(self):
        """
        Verifies that user can add Word Cloud component on Studio and LMS
        """
        section_name = 'Section :{}'.format(uuid4().hex)
        self.studio_course_outline.add_section_with_name(section_name)
        self.assertIn(
            section_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value'
            ).text
        )

        subsection_name = 'Subsection :{}'.format(uuid4().hex)
        self.studio_course_outline.add_subsection_with_name(
            subsection_name
        )
        self.assertIn(
            subsection_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value'
            ).text
        )

        self.studio_course_outline.click_add_unit_button()
        self.unit_container_page.wait_for_page()

        self.unit_container_page.add_word_cloud_component(True)
        word_cloud_data_locator = get_data_locator(
            self.unit_container_page
        )

        # View Live
        self.unit_container_page.view_live_version()
        self.lms_courseware.wait_for_page()
        self.assertEqual(
            word_cloud_data_locator,
            get_data_locator(self.lms_courseware)
        )
        # Remove the added section
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()

    def test_custom_js_display_advanced_component(self):
        """
        Verifies that user can add Custom JavaScript Display and Grading
        component on Studio and LMS
        """
        section_name = 'Section :{}'.format(uuid4().hex)
        self.studio_course_outline.add_section_with_name(section_name)
        self.assertIn(
            section_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value').text
        )

        subsection_name = 'Subsection :{}'.format(uuid4().hex)
        self.studio_course_outline.add_subsection_with_name(
            subsection_name
        )
        self.assertIn(
            subsection_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value').text
        )

        self.studio_course_outline.click_add_unit_button()
        self.unit_container_page.wait_for_page()

        self.assertEqual(
            self.unit_container_page.add_custom_js_display_and_grading(),
            'Custom JavaScript Display and Grading'
        )

        studio_custom_js = get_data_id_of_component(
            self.unit_container_page
        )

        # Publish Unit
        self.studio_course_outline.publish()
        # View Live
        self.unit_container_page.view_live_version()
        self.assertEqual(
            studio_custom_js,
            get_data_id_of_component(self.lms_courseware)
        )
        # Remove the added section
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()
