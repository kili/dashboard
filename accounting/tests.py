from accounting import managers
from accounting import transactions
from django.conf import settings
from django import test
import random


class SimpleTest(test.TestCase):

    def setUp(self):
        self.account_manager = managers.AccountManager()
        self.user_transactions = transactions.UserTransactions()
        self.transaction_history = transactions.TransactionHistory()
        self.user_id = "{0:32x}".format(random.getrandbits(128))
        self.user_account = self.account_manager.get_user_account(
            self.user_id)
        self.asset_source_account = self.account_manager.get_account(
            settings.ACCOUNTING_ASSET_SOURCES[0])
        self.revenue_account = self.account_manager.get_account(
            settings.ACCOUNTING_REVENUE_ACCOUNT)
        self.promotions_account = self.account_manager.get_account(
            settings.ACCOUNTING_PROMOTIONS_ACCOUNT)

    def test_account_charging(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 30)
        self.assertEqual(self.user_account.balance(), 30)
        self.assertEqual(self.asset_source_account.balance(), 30)

    def test_account_positivity(self):
        self.assertEqual(self.user_account.positive_credit, True)
        self.assertEqual(self.revenue_account.positive_credit, True)
        self.assertEqual(self.asset_source_account.positive_credit, False)
        self.assertEqual(self.promotions_account.positive_credit, False)

    def test_consume_user_money(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 150)
        self.user_transactions.consume_user_money(self.user_id, 100, 'cpu')
        self.assertEqual(self.user_account.balance(), 50)
        self.assertEqual(self.revenue_account.balance(), 100)

    def test_transaction_history(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 150)
        self.user_transactions.consume_user_money(self.user_id, 100, 'cpu')
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id)[0]["amount"], -150)
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id, user_values=True)[0]["amount"], 150)
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id)[1]["amount"], 100)
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id)[1]["description"], "resource usage: cpu")

    def test_transaction_history_pagination(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 1)
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 2)
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 3)
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 4)
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 5)
