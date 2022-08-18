import logging

from unittest import TestCase

from src.tooGoodToGoNotifier.notifierSender import EmailNotifier


class EmailSenderTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.email_sender = EmailNotifier(['zywkoszymon@gmail.com',])

    def testSendOneEmailSuccess(self):
        self.email_sender.notify("Hello world3")
        pass

