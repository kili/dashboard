from accounting import managers
from accounting import transactions
from django.conf import settings
from django import test
import random


class SimpleTest(test.TestCase):
    def setUp(self):
        self.account_manager = managers.AccountManager()
        self.user_transactions = transactions.UserTransactions()
        self.asset_source_account = self.account_manager.get_account(
            settings.ACCOUNTING_ASSET_SOURCES[0]
        )
        self.user = "{0:x}".format(random.getrandbits(128))
        self.user_account = self.account_manager.get_account(
            settings.ACCOUNTING_USER_ACCOUNT_FORMAT['format'].format(
                self.user))

    def test_account_charging(self):
        self.user_transactions.receive_user_payment(
            self.user,
            self.asset_source_account.name,
            30)
        self.assertEqual(self.user_account.balance(), 30)
        self.assertEqual(self.asset_source_account.balance(), 30)
