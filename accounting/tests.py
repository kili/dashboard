from accounting import managers
from accounting import transactions
from django.conf import settings
from django import test
import random


class SimpleTest(test.TestCase):

    def setUp(self):
        self.account_manager = managers.AccountManager()
        self.book_manager = managers.BookManager()
        self.user_transactions = transactions.UserTransactions()
        self.transaction_history = transactions.TransactionHistory()
        self.user_id = "{0:032x}".format(random.getrandbits(128))
        self.user_account = self.account_manager.get_user_account(
            self.user_id)
        self.asset_source_account = self.account_manager.get_account(
            settings.ACCOUNTING_ASSET_SOURCES[0])
        self.revenue_account = self.account_manager.get_account(
            settings.ACCOUNTING_REVENUE_ACCOUNT)
        self.promotions_account = self.account_manager.get_account(
            settings.ACCOUNTING_PROMOTIONS_ACCOUNT)

    def test_receive_user_payment(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 30, "TESTS")
        self.assertEqual(self.user_account.balance(), 30)
        self.assertEqual(self.asset_source_account.balance(), 30)

    def test_consume_user_money(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 150, "TESTS")
        self.user_transactions.consume_user_money(self.user_id, 100,
                                                  'you have used resources')
        self.assertEqual(self.user_account.balance(), 50)
        self.assertEqual(self.revenue_account.balance(), 100)

    def test_grant_user_promotion(self):
        self.user_transactions.grant_user_promotion(
            self.user_id, 100, 'free money!')
        self.assertEqual(self.promotions_account.balance(), 100)
        self.assertEqual(self.user_account.balance(), 100)

    def test_promotion_message(self):
        self.user_transactions.grant_user_promotion(
            self.user_id, 100, "free money!")
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id)[0]["description"], "free money!")

    def test_transaction_history(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 150, "TESTS")
        self.user_transactions.consume_user_money(
            self.user_id, 100, 'you have used resources')

        # check values of first transaction
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id))[0]["amount"], -150)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id), user_values=False)[0]["amount"], -150)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id), user_values=True)[0]["amount"], 150)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                self.asset_source_account.name)[0]["amount"], 150)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                self.asset_source_account.name,
                user_values=False)[0]["amount"], 150)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                self.asset_source_account.name,
                user_values=True)[0]["amount"], 150)

        # check values of second transaction
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id))[1]["amount"], 100)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id), user_values=False)[1]["amount"], 100)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id), user_values=True)[1]["amount"], -100)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_REVENUE_ACCOUNT)[0]["amount"], -100)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_REVENUE_ACCOUNT, user_values=False
            )[0]["amount"], -100)
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_REVENUE_ACCOUNT, user_values=True
            )[0]["amount"], 100)

        # check the transaction description messages
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id))[0]["description"],
            "TESTS")
        self.assertEqual(
            self.transaction_history.get_account_transaction_history(
                settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                    self.user_id))[1]["description"],
            'you have used resources')

    def test_user_transaction_history(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 150, "TESTS")
        self.user_transactions.consume_user_money(self.user_id, 100,
                                                  'you have used resources')
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id)[0]["amount"], -150)

    def test_transaction_history_pagination(self):
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 1, "TESTS")
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 2, "TESTS")
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 3, "TESTS")
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 4, "TESTS")
        self.user_transactions.receive_user_payment(
            self.user_id, self.asset_source_account.name, 5, "TESTS")
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id, paginate=True, coords={"begin": 1, "end": 2}
            )[0]["amount"], -2)
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id, paginate=True, coords={"begin": 1, "end": 2}
            )[-1:][0]["amount"], -2)
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id, paginate=True, coords={"begin": 4, "end": 5}
            )[0]["amount"], -5)
        self.assertEqual(
            self.transaction_history.get_user_account_transaction_history(
                self.user_id, paginate=True, coords={"begin": 1, "end": 5}
            )[-1:][0]["amount"], -5)

    def test_get_book_by_currency(self):
        self.assertEqual(
            self.book_manager.get_book(
                settings.ACCOUNTING_BOOKS.keys()[0]).description,
            settings.ACCOUNTING_BOOKS.values()[0])

    def test_account_name_validation(self):
        valid_account_names = settings.ACCOUNTING_ASSET_SOURCES[:]
        valid_account_names.append(settings.ACCOUNTING_PROMOTIONS_ACCOUNT)
        valid_account_names.append(settings.ACCOUNTING_REVENUE_ACCOUNT)

        for name in valid_account_names:
            self.assertEqual(self.account_manager.name_is_valid(name),
                             True)
        self.assertEqual(self.account_manager.name_is_valid(
            settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                self.user_id)), True)
        self.assertEqual(self.account_manager.name_is_valid(
            settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                self.user_id)[:-1]), False)

    def test_format_user_account(self):
        self.assertEqual(
            self.account_manager.format_user_account(self.user_id),
            settings.ACCOUNTING_USER_ACCOUNT_FORMAT["format"].format(
                self.user_id))

    def test_account_positivity(self):
        self.assertEqual(self.user_account.positive_credit, True)
        self.assertEqual(self.revenue_account.positive_credit, True)
        self.assertEqual(self.asset_source_account.positive_credit, False)
        self.assertEqual(self.promotions_account.positive_credit, False)
