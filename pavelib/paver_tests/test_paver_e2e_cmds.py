from __future__ import absolute_import
import os
from path import Path as path
from pavelib.paver_tests.utils import PaverTestCase
from pavelib.paver_utils import TestRunCommand
from pavelib.paver_consts import TEST_DIR, LOG_DIR, REPORT_DIR


class TestPaverE2ECommands(PaverTestCase):
    """
    Tests for e2e paver commands.
    """
    def setUp(self):
        super(TestPaverE2ECommands, self).setUp()

    def _expected_command(self, test_name='', report_name='report.xml'):
        """
        Returns the expected command according to arguments passed
        """
        root_path = path().abspath()
        test_path = path(os.path.join(
            root_path, TEST_DIR, test_name)).abspath()

        expected_command = [
            "SCREENSHOT_DIR='{}'".format(LOG_DIR),
            "SELENIUM_DRIVER_LOG_DIR='{}'".format(LOG_DIR),
            "pytest",
            test_path,
            "-v",
            "--junit-xml='{}'".format(
                path(os.path.join(REPORT_DIR, report_name)).abspath())
        ]
        return ' '.join(expected_command)

    def test_no_report_name_with_no_test_name(self):
        """
        Verify paver test with no report name and test name given.
        """
        test_run_command = TestRunCommand.command()
        self.assertEqual(test_run_command, self._expected_command())

    def test_custom_report_name_with_no_test_name(self):
        """
        Verify paver test with report name given but test name not given.
        """
        test_run_command = TestRunCommand.command(report_name='custom.xml')
        self.assertEqual(
            test_run_command, self._expected_command(report_name='custom.xml'))

    def test_no_report_name_with_test_name(self):
        """
        Verify paver test with test name given but report name not given.
        """
        test_name = 'lms/test_file.py'
        test_run_command = TestRunCommand.command(test_name=test_name)
        self.assertEqual(test_run_command, self._expected_command(
            test_name=test_name))

        test_name = 'lms/test_file.py:TestClass'
        test_run_command = TestRunCommand.command(test_name=test_name)
        self.assertEqual(test_run_command, self._expected_command(
            test_name=test_name))

        test_name = 'lms/test_file.py:TestClass.test_function'
        test_run_command = TestRunCommand.command(test_name=test_name)
        self.assertEqual(test_run_command, self._expected_command(
            test_name=test_name))

    def test_custom_report_name_with_test_name(self):
        """
        Verify paver test with test and report names given.
        """
        test_name = 'lms/test_file.py'
        report_name = 'custom.xml'
        test_run_command = TestRunCommand.command(
            test_name=test_name, report_name=report_name)

        self.assertEqual(test_run_command, self._expected_command(
            test_name=test_name, report_name=report_name))

        test_name = 'lms/test_file.py:TestClass'
        test_run_command = TestRunCommand.command(
            test_name=test_name, report_name=report_name)

        self.assertEqual(test_run_command, self._expected_command(
            test_name=test_name, report_name=report_name))

        test_name = 'lms/test_file.py:TestClass.test_function'
        test_run_command = TestRunCommand.command(
            test_name=test_name, report_name=report_name)

        self.assertEqual(test_run_command, self._expected_command(
            test_name=test_name, report_name=report_name))
