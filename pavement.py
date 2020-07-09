from __future__ import print_function
from __future__ import absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from path import Path as path  # noqa
from pavelib.paver_utils import TestRunCommand, PaverTestCommand  # noqa
from paver.easy import task, needs, consume_args, sh, BuildFailure  # noqa

from pavelib.paver_consts import (
    LOG_DIR,
    REPORT_DIR,
    E2E_TEST_REPORT,
    SCREENSHOT_DIR,
    BASELINE_DIR,
    PAVER_TEST_REPORT_DIR,
    UPLOAD_FILE_DIR,
    WHITE_LABEL_TEST_REPORT,
    ENTERPRISE_TEST_REPORT
)  # noqa


@task
def configure_e2e_tests_pre_reqs():

    # Make sure environment variables are set.
    env_vars = [
        'BASIC_AUTH_USER',
        'BASIC_AUTH_PASSWORD',
        'USER_LOGIN_EMAIL',
        'USER_LOGIN_PASSWORD',
        'COURSE_ORG',
        'COURSE_NUMBER',
        'COURSE_RUN',
        'COURSE_DISPLAY_NAME'
        ]
    for env_var in env_vars:
        try:
            os.environ[env_var]
        except Exception:
            raise BuildFailure(
                "Please set the environment variable :" + env_var)

    # Set environment variables for screen shots.
    os.environ['NEEDLE_OUTPUT_DIR'] = SCREENSHOT_DIR
    os.environ['NEEDLE_BASELINE_DIR'] = BASELINE_DIR
    os.environ['UPLOAD_FILE_DIR'] = UPLOAD_FILE_DIR

    # Create log directory
    LOG_DIR.makedirs_p()

    # Create report directory
    REPORT_DIR.makedirs_p()


@task
@needs('configure_e2e_tests_pre_reqs')
@consume_args
def e2e_test(args):
    sh(TestRunCommand.command(E2E_TEST_REPORT, args))


@task
def create_paver_report_directory():
    PAVER_TEST_REPORT_DIR.makedirs_p()


@task
@needs('create_paver_report_directory')
@consume_args
def paver_cmd_test(args):
    commandline_arg = ''
    if not not args:
        commandline_arg = path(args[0])
    sh(PaverTestCommand.command(commandline_arg, 'paver_cmd_report.xml'))


@task
def wl_test_config():

    # Make sure environment variables are set.
    env_vars = [
        'GLOBAL_PASSWORD'
        ]
    for env_var in env_vars:
        try:
            os.environ[env_var]
        except Exception:
            raise BuildFailure(
                "Please set the environment variable :" + env_var)

    # Set environment variables for screen shots.
    os.environ['NEEDLE_OUTPUT_DIR'] = SCREENSHOT_DIR
    os.environ['NEEDLE_BASELINE_DIR'] = BASELINE_DIR
    os.environ['UPLOAD_FILE_DIR'] = UPLOAD_FILE_DIR

    # Create log directory
    LOG_DIR.makedirs_p()

    # Create report directory
    REPORT_DIR.makedirs_p()


@task
@needs('wl_test_config')
@consume_args
def e2e_wl_test(args):
    sh(TestRunCommand.command(WHITE_LABEL_TEST_REPORT, args, test_type='wl'))


@task
def configure_enterprise_tests_pre_reqs():

    # Make sure environment variables are set.
    env_vars = [
        'BASIC_AUTH_USER',
        'BASIC_AUTH_PASSWORD',
        'ENT_PORTAL_USERNAME',
        'ENT_PORTAL_PASSWORD',
        'ENT_COURSE_TITLE',
        'ENT_COURSE_ORG',
        'ENT_COURSE_PRICE',
        'ENT_COURSE_START_DATE'
        ]
    for env_var in env_vars:
        try:
            os.environ[env_var]
        except Exception:
            raise BuildFailure(
                "Please set the environment variable :" + env_var)

    # Set environment variables for screen shots.
    os.environ['NEEDLE_OUTPUT_DIR'] = SCREENSHOT_DIR
    os.environ['NEEDLE_BASELINE_DIR'] = BASELINE_DIR
    os.environ['UPLOAD_FILE_DIR'] = UPLOAD_FILE_DIR

    # Create log directory
    LOG_DIR.makedirs_p()

    # Create report directory
    REPORT_DIR.makedirs_p()


@task
@needs('configure_enterprise_tests_pre_reqs')
@consume_args
def enterprise_test(args):
    sh(
        TestRunCommand.command(
            ENTERPRISE_TEST_REPORT,
            args,
            test_type='enterprise'
        )
    )
