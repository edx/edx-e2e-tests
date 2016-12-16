"""
Email Client for reading emails
"""
import time
import datetime
from tempmail import TempMail
from guerrillamail import GuerrillaMailSession

from regression.pages.whitelabel.const import (
    EMAIL_SENDER_ACCOUNT,
    INITIAL_WAIT_TIME,
    TIME_OUT_LIMIT,
    WAIT_TIME
)


class MailException(Exception):
    """
    Exceptions for Mail failures
    """
    pass


def yesterday_date():
    """
    Get and return yesterday's date in dd-mmm-yyyy format
    """
    return (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")


class TempMailApi(object):

    def __init__(self):
        self.session = TempMail()

    def get_email_account(self, user_name):
        """
        This function will create an account on TempMail using given user name and first
        of the available domains. The email address created by joining user name and domain
        is returned
        :param user_name:
        :return: email address:
        """
        self.session.login = user_name
        self.session.domain = self.session.available_domains[0]
        return self.session.get_email_address()

    def get_email_text(self, pattern):
        """
        This function will check the availability MIT enrollment email at TempMail server at the
        intervals of 5 seconds and if the email is found it's text is returned.
        If the email is not found after 40 seconds, this function will raise and error
        :param pattern:
        :return: email text
        """
        email_text = ""
        t_end = time.time() + TIME_OUT_LIMIT
        # Run the loop for a pre defined time
        time.sleep(INITIAL_WAIT_TIME)
        while time.time() < t_end:
            try:
                # Check that mail box is not empty
                tmp_email = self.session.get_mailbox()
                if not isinstance(tmp_email, list):
                    raise MailException
                if tmp_email[-1]['mail_from'] != EMAIL_SENDER_ACCOUNT:
                    raise MailException
                # Fetch the email text and stop the loop
                email_text = tmp_email[-1]['mail_text']
                if pattern not in email_text:
                    raise MailException
                break
            except MailException:
                time.sleep(WAIT_TIME)
        if email_text:
            return email_text
        else:
            raise MailException('No Email from ' + EMAIL_SENDER_ACCOUNT)


class GuerrillaMailApi(object):

    def __init__(self):
        self.session = GuerrillaMailSession()

    def get_email_account(self, user_name):
        """
        This function will create an account on GuerrillaMail using given user name and first
        of the available domains. The email address created by joining user name and domain
        is returned
        :param user_name:
        :return: email address:
        """
        self.session.set_email_address(user_name)
        return self.session.get_session_state()['email_address']

    def get_email_text(self, pattern):
        """
        This function will check the availability MIT enrollment email at GuerrillaMail server at the
        intervals of 5 seconds and if the email is found it's text is returned.
        If the email is not found after 40 seconds, this function will raise and error
        :param pattern:
        :return: email text
        """
        email_text = ""
        t_end = time.time() + TIME_OUT_LIMIT
        # Run the loop for a pre defined time
        time.sleep(INITIAL_WAIT_TIME)
        while time.time() < t_end:
            try:
                # Check that mail box is not empty
                email_list = self.session.get_email_list()
                if not email_list:
                    # raise an exception that waits 3 seconds before restarting loop
                    raise MailException
                # Get the email id of last email in the inbox
                email_id = email_list[0].guid
                # if last email is not sent by MIT raise the exception
                email = self.session.get_email(email_id)
                if email.sender != EMAIL_SENDER_ACCOUNT:
                    raise MailException
                # Fetch the email text and stop the loop
                email_text = email.body
                if pattern not in email_text:
                    raise MailException
                break
            except MailException:
                time.sleep(WAIT_TIME)
        if email_text:
            return email_text
        else:
            raise MailException('No Email from ' + EMAIL_SENDER_ACCOUNT)