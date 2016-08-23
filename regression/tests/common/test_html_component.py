"""
End to end tests for HTML Componenets
"""
import os
from uuid import uuid4

from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.pages.studio.unit_page import UnitPageExtended
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.pages.lms.login_lms import LmsLogin
from edxapp_acceptance.pages.lms.courseware import CoursewarePage
from regression.tests.helpers import (
    LoginHelper, get_course_info, get_data_id_of_component
)

from edxapp_acceptance.pages.studio.utils import add_components


class StudioLmsHTMLTest(WebAppTest):
    """
    HTML Components tests that require lms verification with studio
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioLmsHTMLTest, self).setUp()
        # Login to Lms first to avoid authentication problems
        self.login_page = LmsLogin(self.browser)
        LoginHelper.login(self.login_page)

        self.unit_container_page = UnitPageExtended(
            self.browser, None
        )

        self.studio_login_page = StudioLogin(self.browser)
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePageExtended(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

        self.lms_courseware = CoursewarePage(self.browser, self.course_info)

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
                css='.incontext-editor-value').text
        )

        subsection_name = 'Subsection :{}'.format(uuid4().hex)
        self.studio_course_outline.add_subsection_with_name(
            subsection_name)
        self.assertIn(
            subsection_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value').text
        )

        self.studio_course_outline.add_unit()
        self.unit_container_page.wait_for_page()

        # Components to be added
        components = [
            'Text',
            'Announcement',
            'Anonymous User ID',
            'Full Screen Image Tool',
            'IFrame Tool',
            'Zooming Image Tool',
            'Raw HTML'
        ]
        # Add components
        add_components(self.unit_container_page, 'html', components)
        problems = [
            x_block.name for x_block in
            self.unit_container_page.xblocks[1:]
        ]

        # Assert that components appear in same order as added.
        self.assertEqual(problems, components)

        studio_html_components = get_data_id_of_component(
            self.unit_container_page
        )

        # Publish Unit
        self.studio_course_outline.publish()
        # View Live
        self.unit_container_page.view_live_version()
        self.assertEqual(
            studio_html_components,
            get_data_id_of_component(self.lms_courseware)
        )

        # Remove this after addCleanup is added for all tests
        # Cleanup test
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()


class StudioLmsAdvancedComponentTest(WebAppTest):
    """
    Advanced Components tests that require lms verification with studio
    """

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(StudioLmsAdvancedComponentTest, self).setUp()
        # Login to Lms first to avoid authentication problems
        self.login_page = LmsLogin(self.browser)
        LoginHelper.login(self.login_page)

        self.unit_container_page = UnitPageExtended(
            self.browser, None
        )

        self.studio_login_page = StudioLogin(self.browser)
        self.studio_login_page.visit()
        self.studio_login_page.login(self.DEMO_COURSE_USER,
                                     self.DEMO_COURSE_PASSWORD)
        self.studio_home_page = DashboardPageExtended(self.browser)

        self.course_info = get_course_info()

        self.studio_course_outline = CourseOutlinePageExtended(
            self.browser, self.course_info['org'], self.course_info['number'],
            self.course_info['run'])

        self.lms_courseware = CoursewarePage(self.browser, self.course_info)

    def test_word_cloud_advanced_components(self):
        """
        Verifies that user can add Word Cloud components on Studio and LMS
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
            subsection_name)
        self.assertIn(
            subsection_name,
            self.studio_course_outline.q(
                css='.incontext-editor-value').text
        )

        self.studio_course_outline.add_unit()
        self.unit_container_page.wait_for_page()

        self.unit_container_page.add_word_cloud_component()

        studio_word_cloud = get_data_id_of_component(
            self.unit_container_page
        )

        # Publish Unit
        self.studio_course_outline.publish()
        # View Live
        self.unit_container_page.view_live_version()
        self.assertEqual(
            studio_word_cloud,
            get_data_id_of_component(self.lms_courseware)
        )
        # Remove this after addCleanup is added for all tests
        # Cleanup test
        self.studio_course_outline.visit()
        self.studio_course_outline.delete_section()
