from typing import List


class NotifierSender:

    def notify(self, message):
        pass


class EmailNotifier(NotifierSender):

    def __init__(self, emailsToNotify: List):
        self.emailsToNotify = emailsToNotify

    def notify(self, message):
        for email in self.emailsToNotify:
            self._send_email(email, message)

    def _send_email(self, email, message):
        pass
