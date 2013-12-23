"""
Test fixtures for LMS and Studio.
"""
import os
from abc import ABCMeta, abstractmethod
from fabric.api import sudo, settings, execute, env, hide
from fabric.network import disconnect_all
from bok_choy.web_app_fixture import WebAppFixture, WebAppFixtureError


class RemoteCommandFixture(WebAppFixture):
    """
    A fixture created by executing ssh commands on the remote host.
    """

    __metaclass__ = ABCMeta

    def __init__(self, hostname, ssh_user=None, ssh_keyfile=None):
        """
        Configure the fixture to execute on `hostname`.

        `ssh_user` is the account to log in with via ssh
        `ssh_keyfile` is the full path to the private ssh key
        """
        self.hostname = hostname
        self.ssh_user = ssh_user
        self.ssh_keyfile = ssh_keyfile

    def install(self):
        """
        Execute ssh commands on the remote host.
        """
        try:
            env.key_filename = self.ssh_keyfile

            if self.ssh_user is not None:
                host = "{0}@{1}".format(self.ssh_user, self.hostname)
            else:
                host = self.hostname

            with hide('output', 'running'):
                execute(self.execute, hosts=[host])

        finally:
            with hide('output', 'running'):
                disconnect_all()

    @abstractmethod
    def execute(self):
        """
        Execute commands on the remote host using Fabric.
        """
        pass

    def cmd(self, *args):
        """
        Helper method to construct a command string from component args.
        """
        return u" ".join([u"{0}".format(val) for val in args])


class UserFixture(RemoteCommandFixture):
    """
    Ensure that a user exists.
    """

    def __init__(
        self, username, email, password,
        enrollment_mode="honor", course=None, is_staff=False):
        """
        Specify the required `username`, `password`, and `email` for
        the new account.

        `course` is the ID of the course to register the student in;
        if omitted, do not enroll the student in any course.

        `is_staff` is a boolean; if true, indicates that the user is a staff member.
        (Note that this is different than being an instructor or course staff!)

        `enrollment_mode` is either "honor", "verified", or "audit"
        """
        super(UserFixture, self).__init__(
            os.environ['test_host'],
            ssh_user=os.environ.get('ssh_user'),
            ssh_keyfile=os.environ.get('ssh_keyfile')
        )
        self.username = username
        self.password = password
        self.email = email
        self.enrollment_mode = enrollment_mode
        self.course = course
        self.is_staff = is_staff

    def execute(self):
        """
        Use a Django management command to create a user.
        This operation is idempotent.
        """
        command = self.cmd(
            'SERVICE_VARIANT=lms', '/edx/app/edxapp/venvs/edxapp/bin/python',
            '/edx/app/edxapp/edx-platform/manage.py', 'lms', '--settings=aws',
            'create_user', '-u', self.username, '-e', self.email, '-p', self.password,
            '-m', self.enrollment_mode
        )

        if self.is_staff:
            command = self.cmd(command, '-s')

        if self.course is not None:
            command = self.cmd(command, "-c", self.course)

        with settings(sudo_user='edxapp'):
            result = sudo(command)
            if result.failed:
                raise WebAppFixtureError(result)
