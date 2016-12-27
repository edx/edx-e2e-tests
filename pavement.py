import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from path import Path as path
from paver.easy import task, needs, consume_args, sh, BuildFailure
import requests
import StringIO
from zipfile import ZipFile

from pavelib.paver_consts import (
    LOG_DIR,
    REPORT_DIR,
    E2E_TEST_REPORT,
    SCREENSHOT_DIR,
    BASELINE_DIR,
    PAVER_TEST_REPORT_DIR,
    UPLOAD_FILE_DIR
)
from pavelib.paver_utils import NoseCommand, PaverTestCommand


@task
def install_pages():
    """
    Installs page object from edx-platform repo
    """
    repo_root = path(__file__).dirname()
    # Path to store the repo
    lib_path = path(os.path.join(repo_root, 'lib'))
    lib_common_path = path(os.path.join(lib_path, 'edx-platform-master', 'common'))

    # Path to setup.py of pages package
    page_obj_setup_path = path(os.path.join(lib_common_path, 'test', 'acceptance', 'setup.py'))
    xmodule_path = path(os.path.join(lib_common_path, 'lib', 'xmodule'))
    capa_path = path(os.path.join(lib_common_path, 'lib', 'capa'))

    # Download a zipfile of the edx-platform repo to unzip locally.
    # We do this because there is no way via pip to clone with a
    # depth of 1 when installing. And the edx-platform repo is HUGE.
    print 'Downloading the edx-platform repo'
    zip_file_url = 'https://github.com/edx/edx-platform/archive/master.zip'
    response = requests.get(zip_file_url, stream=True)
    archive = ZipFile(StringIO.StringIO(response.content))

    # Also, we only need to extract the page objects, capa, and xmodule.
    print 'Extracting page objects, capa, and xmodule from the edx-platform repo'
    relative_common_path = 'edx-platform-master/common/'
    acceptance_folder = '{}test/acceptance'.format(relative_common_path)
    xmodule_folder = '{}lib/xmodule'.format(relative_common_path)
    capa_folder = '{}lib/capa'.format(relative_common_path)
    for file in archive.namelist():
        if file.startswith(acceptance_folder) or file.startswith(capa_folder) or file.startswith(xmodule_folder):
            archive.extract(file, lib_path)

    print 'Installing the Page Objects'
    sh("python {setup} install".format(setup=page_obj_setup_path))
    print 'Installing capa'
    sh("cd {path_capa}; python setup.py install".format(path_capa=capa_path))
    print 'Installing xmodule'
    sh("cd {path_xmodule}; python setup.py install".format(path_xmodule=xmodule_path))


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
        except:
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
    commandline_arg = ''
    if not not args:
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
