from accounting import managers
from django.conf import settings


class UserTransactions():

    def __init__(self):
        self.account_manager = managers.AccountManager()

    def receive_user_payment(self, user, asset_source, amount):
        if not self.account_manager.is_asset_source(asset_source):
            raise Exception(
                u"'{0}' is invalid asset source".format(asset_source))
        asset_source = self.account_manager.get_account(asset_source)
        user_account = self.account_manager.get_user_account(user)
        asset_source.debit(
            amount,
            user_account,
            u"received payment from {0}".format(asset_source))

    def consume_user_money(self, user, amount, resource):
        user_account = self.account_manager.get_user_account(user)
        revenue_account = self.account_manager.get_revenue_account()
        user_account.debit(
            amount,
            revenue_account,
            u"resource usage: {0}".format(resource))

    def grant_user_promotion(self, user, amount, message):
        user_account = self.account_manager.get_user_account(user)
        promotion_account = self.account_manager.get_promotions_account()
        user_account.credit(
            amount,
            promotion_account,
            message)


class TransactionHistory():

    def account_transaction_history(
            self, account, paginate=False, coords=None):
        """
        If paginate is true, coords must contain
        the keys 'limit' and 'offset'.
        """

