"""
Commands for setting up test environments and running tests.
"""

import os
from ConfigParser import SafeConfigParser
from fabric.api import task, local, lcd
from textwrap import dedent
from path import path
import requests


REPO_ROOT = path(__file__).dirname()
REQUIREMENTS_PATH = REPO_ROOT / "requirements" / "local.txt"
LIB_PATH = REPO_ROOT / "lib"
PAGE_OBJ_SETUP_PATH = LIB_PATH / "edx-platform" / "common" / "test" / "acceptance" / "setup.py"

# Path to the config file (defaults to config.ini, but can be overridden by the environment)
CONFIG_PATH = os.environ.get("CONFIG_PATH", REPO_ROOT / "config.ini")

# Directory to save screenshots on failure
SCREENSHOT_DIR = REPO_ROOT / "log"

# Number of tests to run in parallel, set by environment
NUM_PARALLEL = os.environ.get('NUM_PARALLEL', 1)

# Process timeout for test results
PROCESS_TIMEOUT = 600


@task
def config_lms(**kwargs):
    """
    Ensure that lms tests are configured with the keys/values in kwargs (idempotent).
    This is useful for generating config files on the fly (e.g. in Jenkins).
    """
    _set_config('lms', kwargs)


@task
def config_studio(**kwargs):
    """
    Ensure that studio tests are configured with the keys/values in kwargs (idempotent).
    This is useful for generating config files on the fly (e.g. in Jenkins).
    """
    _set_config('studio', kwargs)


@task
def install_pages():
    """
    Install page objects from external repos.
    """
    local("pip install -r {req} --src={lib}".format(req=REQUIREMENTS_PATH, lib=LIB_PATH))
    local("python {setup} install".format(setup=PAGE_OBJ_SETUP_PATH))


@task
def test():
    """
    Run all tests.
    """
    test_lms()
    test_studio()


@task
def test_lms(test_spec=None):
    """
    Execute the LMS tests.
    `test_spec` is a nose-style test specifier (e.g. "test_module.py:TestCase.test_method")
    """
    config = _read_config('lms')
    _abort_if_not_available(config)
    _run_tests(_test_path('tests/lms', test_spec), config)


@task
def test_studio(test_spec=None):
    """
    Execute the Studio tests.
    `test_spec` is a nose-style test specifier (e.g. "test_module.py:TestCase.test_method")
    """
    config = _read_config('studio')
    _abort_if_not_available(config)
    _run_tests(_test_path('tests/studio', test_spec), config)


def _available(url):
    """
    Return a boolean indicating whether `url` is available.
    """
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        return False

    return resp.status_code == 200


def _test_url(config):
    """
    Given a dictionary of configuration values, return a URL for the test host.
    """
    # Make sure that both keys for the auth credentials exist
    # and that their values are not the empty string.
    if 'basic_auth_user' in config and bool(config['basic_auth_user']) \
        and 'basic_auth_password' in config and bool(config['basic_auth_password']):
            return "{protocol}://{basic_auth_user}:{basic_auth_password}@{test_host}".format(**config)

    else:
        return "{protocol}://{test_host}".format(**config)


def _abort_if_not_available(config):
    """
    Use the values in `config` (dict) to check the host and abort if not available.
    """
    url = _test_url(config)
    if not _available(url):
        _abort("{0} is not available".format(url))


def _set_config(suite, options_dict):
    """
    Set the config keys/values to `options_dict` for the test suite `suite`.
    """
    config = SafeConfigParser()
    config.read(CONFIG_PATH)

    print "Updating {0} in '{1}'".format(suite, CONFIG_PATH)

    if not config.has_section(suite):
        print "Adding section '{0}'".format(suite)
        config.add_section(suite)

    for key, val in options_dict.items():
        print "Setting: {0}={1}".format(key, val)
        config.set(suite, key, val)

    with open(CONFIG_PATH, 'wb') as config_file:
        config.write(config_file)


def _read_config(suite):
    """
    Read the config ini file for the test suite `suite`
    (identified as a group in the config)

    Returns a dictionary of configuration values that will
    be passed as environment variables to the test suite.
    """
    if not os.path.isfile(CONFIG_PATH):
        msg = """
            Could not find config file at '{0}'.
            Please set the CONFIG_PATH environment variable
        """.format(CONFIG_PATH)
        _abort(msg)

    config = SafeConfigParser()
    config.read(CONFIG_PATH)

    result = {
        key: config.get(suite, key) for key in config.options(suite)
    }

    # Validate the required keys
    for key in ['protocol', 'test_host']:
        if key not in result:
            _abort("Missing '{0}' in config file.".format(key))

    return result


def _test_path(test_package, test_spec):
    """
    Return the absolute path to the Python package `test_package`
    and append the nose-style test specifier `test_spec`.
    """
    test_path = str(REPO_ROOT / test_package)

    if test_spec is not None:
        test_path += "/" + test_spec

    return test_path


def _run_tests(test_path, config):
    """
    Assemble the test runner command and execute it.

    `test_path` is the path in which the tests are located
        Use this to restrict execution to a particular set of tests.

    `test_spec` is a nose-style test identifier, used to run a subset of tests.
    """

    cmd_to_execute = _cmd('SCREENSHOT_DIR={}'.format(SCREENSHOT_DIR), 'nosetests', test_path)

    # Add a special environment variable for the test host URL
    cmd_to_execute = _cmd("test_url=" + _test_url(config), cmd_to_execute)

    # Expose configuration options as environment variables
    for key, val in config.iteritems():
        cmd_to_execute = _cmd("{0}={1}".format(key, val), cmd_to_execute)

    # Configure the tests to run in parallel
    if NUM_PARALLEL > 1:
        cmd_to_execute = _cmd(
            cmd_to_execute,
            '--processes={0}'.format(NUM_PARALLEL),
            '--process-timeout={0}'.format(PROCESS_TIMEOUT)
        )

    local(cmd_to_execute)


def _cmd(*args):
    """
    Helper to construct a command string from
    a list of components.
    """
    return ' '.join(args)


def _abort(msg):
    """
    Helper to abort with a message.
    """
    print "ABORT: " + dedent(msg).strip()
    exit(1)
