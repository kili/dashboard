from accounting import accounts
from django.conf import settings


class TransactionManager():

    def __init__(self):
        self.account_manager = accounts.AccountManager()

    def receive_user_payment(self, user, asset_source, amount):
        if not asset_source in settings.ACCOUNTING_ASSET_SOURCES:
            raise Exception(
                "'{0}' is invalid asset source".format(asset_source))
        asset_source = self.account_manager.get_account(asset_source)
        user_account = \
            self.account_manager.get_account("USER_{0}".format(user))
        asset_source.debit(
            amount,
            user_account,
            "received payment from {0}".format(asset_source))

    def consume_user_money(self, user, amount, resource):
        user_account = self.account_manager.get_account("USER_{0}".format(user))
        revenue_account = self.account_manager.get_account("REVENUE")
        user_account.debit(
            amount,
            revenue_account,
            "resource usage: {0}".format(resource))

