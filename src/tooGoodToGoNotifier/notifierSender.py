import logging
import os
import smtplib
import ssl
from typing import List

from dotenv import load_dotenv


class NotifierSender:

    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)

    def notify(self, message):
        pass


class EmailNotifier(NotifierSender):

    def __init__(self, emailsToNotify: List):
        super().__init__()
        self.emailsToNotify = emailsToNotify

    def notify(self, message):
        for email in self.emailsToNotify:
            self._send_email(email, message)
            self.logger.info(f"Send email to: {email}")

    def _send_email(self, receiver, message):
        port = os.getenv('PORT')
        smtp_server = os.getenv('SMTP_SERVER')
        password = os.getenv('GMAIL_PASSWORD')
        sender_email = os.getenv('GMAIL_LOGIN')
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, int(port)) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(sender_email, password)
            return server.sendmail(sender_email, receiver, message)

        pass
