import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from path import Path as path
from pavelib.paver_utils import NoseCommand
from paver.easy import task, needs, consume_args, sh, BuildFailure

from pavelib.paver_consts import (
    LOG_DIR,
    REPORT_DIR,
    SMOKE_TEST_REPORT,
    SCREENSHOT_DIR,
    BASELINE_DIR
)


@task
def check_env_vars():
    env_vars = [
        'BASIC_AUTH_USER',
        'BASIC_AUTH_PASSWORD',
        'USER_LOGIN_EMAIL',
        'USER_LOGIN_PASSWORD'
        ]
    for env_var in env_vars:
        try:
            os.environ[env_var]
        except:
            raise BuildFailure("Please set the environment variable :" + env_var)


@task
def set_screenshots_path():
    os.environ['NEEDLE_OUTPUT_DIR'] = SCREENSHOT_DIR
    os.environ['NEEDLE_BASELINE_DIR'] = BASELINE_DIR


@task
def create_log_directory():
    LOG_DIR.makedirs_p()


@task
def create_reports_directory():
    REPORT_DIR.makedirs_p()


@task
@needs('check_env_vars', 'set_screenshots_path', 'create_log_directory', 'create_reports_directory')
@consume_args
def smoke_test(args):
    commandline_arg = path(args[0])
    sh(NoseCommand.command(SMOKE_TEST_REPORT, commandline_arg))
