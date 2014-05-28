from accounting import managers
from accounting import transactions
from django import test


class SimpleTest(test.TestCase):
    def setUp(self):
        self.account1 = managers.AccountManager().get_account("account1")
        self.account2 = managers.AccountManager().get_account("account2")
        self.stripe = managers.AccountManager().get_account("STRIPE")
        self.user_transactions = transactions.UserTransactions()

    def test_account_charging(self):
        self.user_transactions.receive_user_payment(
            self.account1.name,
            "STRIPE",
            30)
        self.assertEqual(self.account1.balance(), 30)
        self.assertEqual(self.stripe.balance(), 30)
