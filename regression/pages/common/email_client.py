"""
Email Client for reading emails
"""
import time
import datetime
import imaplib
import email

from regression.pages.whitelabel.const import (
    DEFAULT_TEST_EMAIL_ACCOUNT,
    EMAIL_SENDER_ACCOUNT,
    INITIAL_WAIT_TIME,
    TEST_EMAIL_PASSWORD,
    TEST_EMAIL_SERVICE,
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


class MailClient(object):
    """
    Connect to email client using imap and read mails from Inbox
    """

    def __init__(self):
        self.mail = imaplib.IMAP4_SSL(TEST_EMAIL_SERVICE)

    def login_to_email_account(self):
        """
        Login to email account
        """
        self.mail.login(
            DEFAULT_TEST_EMAIL_ACCOUNT, TEST_EMAIL_PASSWORD)

    def open_inbox(self):
        """
        Open inbox to get the list of emails
        """
        self.mail.list()
        # Out: list of "folders" aka labels in email.
        self.mail.select("inbox")  # connect to inbox.

    def get_latest_email_uid(self, current_email_user, mail_topic):
        """
        This function will check the availability of target email at the
        intervals of 5 seconds and if the email is found it's uuid is returned.
        If the email is not found after predefined period of time seconds,
        this function will raise an error
        Args:
            current_email_user:
            mail_topic:
        Returns:
            email_uuid:
        """
        self.login_to_email_account()
        self.open_inbox()
        latest_email_uid = None
        t_end = time.time() + TIME_OUT_LIMIT
        # Run the loop for a pre defined time
        time.sleep(INITIAL_WAIT_TIME)
        while time.time() < t_end:
            try:
                # Check that target email is present in Inbox
                # The target mail has to satisfy following criteria
                # a) It has to be sent during the last 24 hours (this is used
                # mainly to speed up the search)
                # b) Mail From and Mail To are correct
                # c) The partial subject string is present in the mail subject
                result, data = self.mail.uid(
                    'search',
                    None,
                    '(SENTSINCE {date} HEADER FROM {mail_from} TO '
                    '{mail_to} SUBJECT {mail_subject})'.format(
                        date=yesterday_date(),
                        mail_from=EMAIL_SENDER_ACCOUNT,
                        mail_to=current_email_user,
                        mail_subject=mail_topic
                    )
                )
                if not result:
                    raise MailException
                # Get the uid of last email that satisfies the criteria
                latest_email_uid = data[0].split()[-1]
                break
            except MailException:
                time.sleep(WAIT_TIME)
        if latest_email_uid:
            return latest_email_uid
        else:
            raise MailException('No Email matching the search criteria')

    def get_email_message(self, current_email_user, mail_topic):
        """
        Get the text message from Email
        Args:
            current_email_user:
            mail_topic:
        Returns:
            email text:
        """
        resulting_data = self.mail.uid(
            'fetch',
            self.get_latest_email_uid(current_email_user, mail_topic),
            '(RFC822)'
        )
        mail_data = resulting_data[1]
        raw_email = mail_data[0][1]
        email_message = email.message_from_string(raw_email)
        return self.get_first_text_block(email_message)

    @staticmethod
    def get_first_text_block(email_message_instance):
        """
        In case of multiple payloads return first text block
        Args:
            email_message_instance:
        """
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()
