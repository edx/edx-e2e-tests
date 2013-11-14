"""
Credentials that will be used for the edX application.
"""


import os
from uuid import uuid4

class InvalidEmailError(Exception):
    """
    Provided email credentials are not in a valid format.
    """
    pass


class TestCredentials(object):
    """
    Encapsulate fake user information.
    """

    def __init__(self):
        """
        Initialize new credentials.
        """

        # Get registration email from the environment (set by the config.ini file)
        reg_email = os.environ.get('registration_email', 'user@example.com')

        try:
            reg_email_user, reg_email_domain = reg_email.split('@')
        except ValueError:
            raise InvalidEmailError("'{0}' is not a valid email address".format(reg_email))

        unique_id = str(uuid4())[0:8]

        self._username = "{0}_{1}".format(reg_email_user, unique_id)
        self._email = "{0}+{1}@{2}".format(reg_email_user, unique_id, reg_email_domain)
        self._full_name = "{0} {1}".format(reg_email_user, unique_id)
        self._password = unique_id

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def full_name(self):
        return self._full_name

    @property
    def password(self):
        return self._password
