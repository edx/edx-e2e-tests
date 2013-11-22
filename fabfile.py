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

# Keys from the config file to use for the availibility check
LMS_KEYS = {'protocol': 'lms_protocol', 'test_host': 'lms_test_host'}
CMS_KEYS = {'protocol': 'cms_protocol', 'test_host': 'cms_test_host'}
MKTG_KEYS = {'protocol': 'protocol', 'test_host': 'test_host'}

@task
def config_edxapp(**kwargs):
    """
    Ensure that edxapp tests are configured with the keys/values in kwargs (idempotent).
    This is useful for generating config files on the fly (e.g. in Jenkins).
    """
    _set_config('edxapp', kwargs)


@task
def config_mktg(**kwargs):
    """
    Ensure that mktg tests are configured with the keys/values in kwargs (idempotent).
    This is useful for generating config files on the fly (e.g. in Jenkins).
    """
    _set_config('mktg', kwargs)


@task
def test_edxapp(test_spec=None, availability_keys=[LMS_KEYS, CMS_KEYS]):
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
    _run_tests(test_path, test_spec, config, availability_keys=availability_keys)


@task
def test_lms(test_case=None):
    """
    Execute only the lms test specs (from the test_lms.py file).

    Optionally specify the test case or method in this form to limit execution
    to that test case or method:

        * "TestCase"
        * "TestCase:test_method"
    """
    if test_case:
        test_spec = 'test_lms.py:{}'.format(test_case)
    else:
        test_spec = 'test_lms.py'
    test_edxapp(test_spec=test_spec, availability_keys=[LMS_KEYS])


@task
def test_cms(test_case=None):
    """
    Execute only the Studio test specs (from the test_cms.py file).

    Optionally specify the test case or method in this form to limit execution
    to that test case or method:

        * "TestCase"
        * "TestCase:test_method"
    """
    if test_case:
        test_spec = 'test_cms.py:{}'.format(test_case)
    else:
        test_spec = 'test_cms.py'
    test_edxapp(test_spec=test_spec, availability_keys=[CMS_KEYS])


@task
def test_mktg(test_spec=None, availability_keys=[MKTG_KEYS]):
    """
    Execute the E2E test suite on an instance of the website administered by marketing.
    See test_edxapp docstring for 'test_spec' explanation and examples.
    """
    config = _read_config('mktg')
    test_path = str(REPO_ROOT / "test_mktg")
    _run_tests(test_path, test_spec, config, availability_keys=availability_keys)


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

    return result


def _run_tests(test_path, test_spec, config, availability_keys=None):
    """
    Assemble the test runner command and execute it.

    `test_path` is the path in which the tests are located
        Use this to restrict execution to a particular set of tests (e.g. edxapp or mktg)

    `test_spec` is a nose-style test identifier, used to run a subset of tests.

    `config` is a dict of configuration values (see `_read_config()` for details)

    `availability_keys` is a list of dicts containing protocol/server key name pairs
        from the config dict that will be used to test that the application is available.
        e.g. [{'protocol': 'protocol', 'test_host': 'test_host'}] or
        [{'protocol': 'lms_protocol', 'test_host': 'lms_test_host'},
         {'protocol': 'cms_protocol', 'test_host': 'cms_test_host'}]
    """
    # Ensure that the service is available before running the test suite
    if availability_keys:
        for keypair in availability_keys:
            if not _available(config[keypair['protocol']], config[keypair['test_host']]):
                _abort("Could not contact '{0}' via {1}".format(
                    config[keypair['test_host']], config[keypair['protocol']]))

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
    exit(1)
