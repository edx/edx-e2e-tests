"""
End to end tests for HTML Components
"""
from uuid import uuid4

from bok_choy.web_app_test import WebAppTest
from bok_choy.promise import BrokenPromise
from edxapp_acceptance.pages.studio.utils import add_components
from edxapp_acceptance.pages.lms.course_nav import CourseNavPage

from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.pages.studio.unit_page import UnitPageExtended
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.lms.utils import get_course_key
from regression.pages.lms.lms_courseware import CoursewarePageExtended
from regression.tests.helpers import (
    StudioLoginApi, get_course_info, get_data_id_of_component, LmsLoginApi,
    get_data_locator, get_data_locator_of_html, get_data_id_of_html
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


class StudioLmsHTMLTest(StudioLmsComponentBaseTest):
    """
    HTML Components tests that require lms verification with studio
    """
    def setUp(self):
        """
        Call setUp in parent
        """
        super(StudioLmsHTMLTest, self).setUp()

    def test_html_components(self):
        """
        Verifies that user can add HTML components on Studio and LMS
        """
        self.studio_course_outline.visit()
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

        # Components to be added
        components = [
            'Text',
            'Announcement',
            'IFrame Tool',
            'Raw HTML'
        ]
        # Add components. A BrokenPromise probably means that we missed the
        # notification. We should just swallow this error and not raise it.
        try:
            add_components(self.unit_container_page, 'html', components)
        except BrokenPromise as _err:
            pass
        problems = [
            x_block.name for x_block in
            self.unit_container_page.xblocks[1:]
        ]

        # Assert that components appear in same order as added.
        self.assertEqual(problems, components)

        studio_html_components = get_data_locator_of_html(
            self.unit_container_page
        )

        # Publish Unit
        self.studio_course_outline.publish()
        # View Live
        self.unit_container_page.view_live_version()
        self.assertEqual(
            studio_html_components,
            get_data_id_of_html(self.lms_courseware)
        )

        # Remove this after addCleanup is added for all tests
        # Cleanup test
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()


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
        self.studio_course_outline.visit()
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

        # Publish Unit
        self.studio_course_outline.publish()

        # View Live
        self.unit_container_page.view_live_version()
        self.lms_courseware.wait_for_page()
        self.assertEqual(
            word_cloud_data_locator,
            get_data_locator(self.lms_courseware)
        )
        # Remove this after addCleanup is added for all tests
        # Cleanup test
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()

    def test_custom_js_display_advanced_component(self):
        """
        Verifies that user can add Custom JavaScript Display and Grading
        component on Studio and LMS
        """
        self.studio_course_outline.visit()
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
        # Remove this after addCleanup is added for all tests
        # Cleanup test
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()


class StudioViewTest(StudioLmsComponentBaseTest):
    """
    HTML Components tests related to 'studio view' of component.
    """
    def setUp(self):
        """
        Call setUp in parent
        """
        super(StudioViewTest, self).setUp()

    def test_unit_studio_view(self):
        """
        Scenario: To test studio view of component from LMS
        Given that I am at the LMS side of the edX.
        And I open a component
        And I click on the 'View unit in Studio' button
        Then correct component should open.
        """
        self.studio_course_outline.visit()
        section_name = 'Section :{}'.format(uuid4().hex)
        subsection_name = 'Subsection :{}'.format(uuid4().hex)
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
        # From LMS, navigate to the section added.
        course_nav = CourseNavPage(self.browser)
        course_nav.go_to_section(section_name, subsection_name)
        # View unit in the studio
        self.lms_courseware.view_unit_in_studio()
        self.unit_container_page.wait_for_page()
        # Correct unit component should open.
        self.assertEqual(
            get_data_locator(self.unit_container_page),
            data_locator, 'Correct component is opened'
        )
        # Remove this after addCleanup is added for all tests.
        # Cleanup test
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()
