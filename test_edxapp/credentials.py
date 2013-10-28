"""
Credentials that will be used for the edX application.
"""


from uuid import uuid4


class TestCredentials(object):
    """
    Encapsulate fake user information.
    """

    BASE_EMAIL_USER = "will"
    EMAIL_DOMAIN = "edx.org"

    def __init__(self):
        """
        Initialize new credentials.
        """

        unique_id = str(uuid4())[0:8]

        self._username = "{0}_{1}".format(
            self.BASE_EMAIL_USER, unique_id
        )

        self._email = "{0}+{1}@{2}".format(
            self.BASE_EMAIL_USER, unique_id, self.EMAIL_DOMAIN
        )

        self._full_name = "{0} {1}".format(
            self.BASE_EMAIL_USER, unique_id
        )

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
