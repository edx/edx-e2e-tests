"""
Test fixtures for LMS and Studio.
"""
import os
from fabric.api import sudo, settings
from e2e_framework.web_app_fixture import RemoteCommandFixture, WebAppFixtureError


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
            os.environ['lms_test_host'],
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
