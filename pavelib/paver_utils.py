from __future__ import absolute_import
from path import Path as path

from .paver_consts import (
    LOG_DIR,
    TEST_DIR,
    REPORT_DIR,
    PAVER_TEST_DIR,
    PAVER_TEST_REPORT_DIR,
    WHITE_LABEL_TEST_DIR,
    ENTERPRISE_TEST_DIR
)


class TestRunCommand(object):
    @staticmethod
    def command(report_name="report.xml", user_args="", test_type=None):
        """
        Construct the pytest command with all path and pytest options and
        return this command to paver tasks (Used for e2e tests)
        """
        arguments = get_file_path_and_other_args(user_args)

        test_directory = TEST_DIR
        if arguments['file_path']:
            test_path = path.joinpath(test_directory, arguments['file_path'][0])
        else:
            if test_type == 'wl':
                test_path = WHITE_LABEL_TEST_DIR
            elif test_type == 'enterprise':
                test_path = ENTERPRISE_TEST_DIR
            else:
                arguments['cmd_args'].extend([
                    '='.join(['--ignore', WHITE_LABEL_TEST_DIR]),
                    '='.join(['--ignore', ENTERPRISE_TEST_DIR]),
                ])
                # Default to running all tests if no specific test is specified
                test_path = test_directory

        # Create report path by concatenating report directory and report name
        report_path = path.joinpath(REPORT_DIR, report_name)

        # Construct the command as a list
        construct_command = [
            "SCREENSHOT_DIR='{}'".format(LOG_DIR),
            "SELENIUM_DRIVER_LOG_DIR='{}'".format(LOG_DIR),
            "pytest",
            test_path,
            "-v",
            "--junit-xml='{}'".format(report_path)
            ]

        construct_command.extend(arguments['cmd_args'])
        cmd = " ".join(construct_command)
        return cmd


class PaverTestCommand(object):

    @staticmethod
    def command(test_name='', report_name='report.xml'):
        """
        Construct the pytest command with all path and pytest options and
        return this command to paver tasks which will be used for
        paver tests located at pavelib/paver_tests.
        """

        # Default to running all tests if no specific test is specified
        if not test_name:
            test_path = PAVER_TEST_DIR
        else:
            test_path = path.joinpath(PAVER_TEST_DIR, test_name)

        # Create report path by concatenating report directory and report name
        report_path = path.joinpath(PAVER_TEST_REPORT_DIR, report_name)

        # Construct the command as a list
        construct_command = [
            "pytest",
            test_path,
            "-v",
            "--junit-xml='{}'".format(report_path)
            ]

        # return command as a string
        cmd = " ".join(construct_command)
        return cmd


def get_file_path_and_other_args(user_cmd_args):
    """
    Extracts path of test file(if any) and other args from command line.

    Arguments:
        user_cmd_args(str): User's command line.

    Returns:
        dict: Contains a key 'file_path' for test file and
              extra arguments in key 'cmd_args'
    """
    cmd_args = []
    file_path = []
    for arg in user_cmd_args:
        if arg[0] == '-':
            cmd_args.append(arg)
        else:
            file_path.append(arg)
    return {
        'cmd_args': cmd_args,
        'file_path': file_path
    }
