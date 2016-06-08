from path import Path as path

from paver_consts import (
    LOG_DIR,
    TEST_DIR,
    REPORT_DIR,
    PAVER_TEST_DIR,
    PAVER_TEST_REPORT_DIR
)


class NoseCommand(object):

    @staticmethod
    def command(report_name="report.xml", test_name=""):
        """
        Construct the nose command with all path and nose options and
        return this command to paver tasks (Used for e2e tests)
        """

        # Default to running all tests if no specific test is specified
        if not test_name:
            test_path = TEST_DIR
        else:
            test_path = path.joinpath(TEST_DIR, test_name)

        # Create report path by concatenating report directory and report name
        report_path = path.joinpath(REPORT_DIR, report_name)

        # Construct the command as a list
        construct_command = [
            "SCREENSHOT_DIR='{}'".format(LOG_DIR),
            "SELENIUM_DRIVER_LOG_DIR='{}'".format(LOG_DIR),
            "nosetests",
            test_path,
            "-v",
            "--with-xunit",
            "--xunit-file='{}'".format(report_path)
            ]
        # return command as a string
        cmd = " ".join(construct_command)
        return cmd


class PaverTestCommand(object):

    @staticmethod
    def command(test_name='', report_name='report.xml'):
        """
        Construct the nose command with all path and nose options and
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
            "nosetests",
            test_path,
            "-v",
            "--with-xunit",
            "--xunit-file='{}'".format(report_path)
            ]

        # return command as a string
        cmd = " ".join(construct_command)
        return cmd
