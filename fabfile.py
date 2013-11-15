"""
Commands for setting up test environments and running tests.
"""

import os
from ConfigParser import SafeConfigParser
from fabric.api import *
from fabric.contrib import files
from textwrap import dedent
from path import path
import requests


REPO_ROOT = path(__file__).dirname()

# Path to the config file (defaults to config.ini, but can be overridden by the environment)
CONFIG_PATH = os.environ.get("CONFIG_PATH", REPO_ROOT / "config.ini")

# Number of tests to run in parallel, set by environment
NUM_PARALLEL = os.environ.get('NUM_PARALLEL_TESTS', 1)

# Process timeout for test results
PROCESS_TIMEOUT = 600


def config_edxapp(**kwargs):
    """
    Ensure that edxapp tests are configured with the keys/values in kwargs (idempotent).
    This is useful for generating config files on the fly (e.g. in Jenkins).
    """
    _set_config('edxapp', kwargs)


def config_mktg(**kwargs):
    """
    Ensure that mktg tests are configured with the keys/values in kwargs (idempotent).
    This is useful for generating config files on the fly (e.g. in Jenkins).
    """
    _set_config('mktg', kwargs)


def test_edxapp(test_spec=None):
    """
    Execute the E2E test suite on an instance of the edxapp.

    `test_spec` is a string of the form:

        * "module.py"
        * "module.py:TestCase"
        * "module.py:TestCase.test_method"

    to run only those tests.  If ommitted, run all the tests.
    """
    config = _read_config('edxapp')
    test_path = str(REPO_ROOT / "test_edxapp")
    _run_tests(test_path, test_spec, config)


def test_mktg(test_spec=None):
    """
    Execute the E2E test suite on an instance of the website administered by marketing.
    See test_edxapp docstring for 'test_spec' explanation and examples.
    """
    config = _read_config('mktg')
    test_path = str(REPO_ROOT / "test_mktg")
    _run_tests(test_path, test_spec, config)


def _available(protocol, hostname):
    """
    Return a boolean indicating whether the host
    at `hostname` is available (success HTTP response)
    """

    try:
        url = "{0}://{1}".format(protocol, hostname)
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        return False

    return resp.status_code == 200


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

    Only `protocol` and `test_host` keys are required.
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

    # Check that the required keys are defined
    missing = []
    for key in ['protocol', 'test_host']:
        if key not in result:
            missing.append(key)

    if len(missing) > 0:
        msg = "Test suite {0} is missing configuration values: {1}".format(
            suite, missing.join(",")
        )
        _abort(msg)

    return result


def _run_tests(test_path, test_spec, config):
    """
    Assemble the test runner command and execute it.

    `test_path` is the path in which the tests are located
        Use this to restrict execution to a particular set of tests (e.g. edxapp or mktg)

    `test_spec` is a nose-style test identifier, used to run a subset of tests.

    `config` is a dict of configuration values (see `_read_config()` for details)
    """

    # Ensure that the service is available before running the test suite
    if not _available(config['protocol'], config['test_host']):
        _abort("Could not contact '{0}'".format(config['test_host']))

    # Restrict to a subset of tests based on command-line arguments
    if test_spec is not None:
        test_path += "/" + test_spec

    cmd_to_execute = _cmd('nosetests', test_path)

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
    exit(0)
