import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from path import Path as path
from pavelib.paver_utils import NoseCommand, PaverTestCommand
from paver.easy import task, needs, consume_args, sh, BuildFailure

from pavelib.paver_consts import (
    LOG_DIR,
    REPORT_DIR,
    E2E_TEST_REPORT,
    SCREENSHOT_DIR,
    BASELINE_DIR,
    PAVER_TEST_REPORT_DIR
)


@task
def install_pages():
    """
    Installs page object from edx-platform repo
    """
    repo_root = path(__file__).dirname()
    # Path to find the git address of repo
    requirement_path = path(os.path.join(
        repo_root, 'requirements', 'local.txt'))
    # Path to store the repo
    lib_path = path(os.path.join(repo_root, 'lib'))
    # Path to setup.py of pages package
    page_obj_setup_path = path(os.path.join(
        lib_path, 'edx-platform', 'common',
        'test', 'acceptance', 'setup.py'))

    print 'Installing the Page Objects'
    sh("pip install -r {req} --src={lib}".format(
        req=requirement_path, lib=lib_path))
    # Install pages
    sh("python {setup} install".format(setup=page_obj_setup_path))


@task
def configure_e2e_tests_pre_reqs():

    # Make sure environment variables are set.
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
            raise BuildFailure(
                "Please set the environment variable :" + env_var)

    # Set environment variables for screen shots.
    os.environ['NEEDLE_OUTPUT_DIR'] = SCREENSHOT_DIR
    os.environ['NEEDLE_BASELINE_DIR'] = BASELINE_DIR

    # Create log directory
    LOG_DIR.makedirs_p()

    # Create report directory
    REPORT_DIR.makedirs_p()


@task
@needs('configure_e2e_tests_pre_reqs')
@consume_args
def e2e_test(args):
    commandline_arg = path(args[0])
    sh(NoseCommand.command(E2E_TEST_REPORT, commandline_arg))


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
