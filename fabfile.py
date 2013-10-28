"""
Commands for setting up test environments and running tests.
"""

from fabric.api import *
from fabric.contrib import files
from textwrap import dedent
from path import path
import requests


# Use SSH config to authenticate with the integration server
# Use ~/.ssh/config to define hosts and login information
env.use_ssh_config = True


REPO_ROOT = path(__file__).dirname()

# Courses that will be imported before running the tests
# These should be .tar.gz archives exported from Studio
COURSE_FIXTURES = [
    ('edx_demo_course', 'edx_demo_course_1_0.tar.gz'),
]


def test_edxapp():
    """
    Execute the E2E test suite on an instance of the edxapp.
    """
    if env.host is None:
        _abort("""
            Abort: Must specify at least one host.
            See http://docs.fabfile.org/en/1.8/usage/execution.html#defining-host-lists
        """)

    # Ensure that the service is available before running the test suite
    if not _available(env.host):
        _abort("Could not contact '{0}'".format(env.host))

    # Run the tests!
    local(_cmd(
        'EDXAPP_HOST=' + env.host,
        'nosetests', REPO_ROOT / "edx_tests" / "tests"
    ))


def install_courses():
    """
    Install course fixtures that the test suite depends on.
    """

    confirm = prompt(
        "Install fixture courses on {0}?".format(env.host),
        default='y',
        validate=lambda x: x.lower() == 'y'
    )

    if not confirm:
        _abort("Cancelled")

    for course_name, course_archive in COURSE_FIXTURES:

        # Upload the course archive if we haven't already
        remote_archive = path('/tmp') / course_archive
        if not files.exists(remote_archive):
            print "Uploading {0}".format(remote_archive)
            local_path = REPO_ROOT / "edx_tests" / "fixtures" / course_archive
            put(str(local_path), str(remote_archive))
        else:
            print "{0} already exists, skipping.".format(remote_archive)

        # Unarchive the course if we haven't already
        remote_data = path('/opt/wwc/data')
        if not files.exists(remote_data / course_name):

            print "Unarchiving {0} to {1}".format(remote_archive, remote_data / course_name)

            # Ensure that the archive has the right owner
            sudo('chown www-data:www-data {0}'.format(remote_archive))

            with settings(sudo_user="www-data"):
                sudo('tar -zxvf {0} -C {1}'.format(remote_archive, remote_data))

        else:
            print "{0} already exists, skipping.".format(remote_data / course_name)

        # Import the course
        # Even if it already exists, this should override
        # any changes that might have been made
        # (We need to cd to the directory because the settings
        # use the git SHA to version assets and will fail to load
        # if we're not in a git repo.)
        with cd('/opt/wwc/edx-platform'):
            sudo(_manage_cmd('cms', 'xlint ../data {0}'.format(course_name)))
            sudo(_manage_cmd('cms', 'import ../data {0}'.format(course_name)))


def _available(hostname):
    """
    Return a boolean indicating whether the host
    at `hostname` is available (success HTTP response)
    """

    try:
        resp = requests.get('http://' + hostname)
    except requests.exceptions.ConnectionError:
        return False

    return resp.status_code == 200


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


def _manage_cmd(env, cmd):
    return _cmd(
        'SERVICE_VARIANT={0}'.format(env),
        '/opt/edx/bin/django-admin.py', cmd,
        '--settings={0}.envs.aws'.format(env),
        '--pythonpath=/opt/wwc/edx-platform'
    )
