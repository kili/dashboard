from accounting import managers
from notifications.notification_sender import Notifications
from thresholds.balance_thresholds import check_thresholds


class UserTransactions():

    def __init__(self):
        self.account_manager = managers.AccountManager()

    @check_thresholds
    def receive_user_payment(self, user, asset_source, amount, comment):
        if not self.account_manager.is_asset_source(asset_source):
            raise Exception(
                u"'{0}' is invalid asset source".format(asset_source))
        self.account_manager.get_user_account(user).credit(
            amount,
            self.account_manager.get_account(asset_source),
            comment)

    @check_thresholds
    def consume_user_money(self, user, amount, msg):
        self.account_manager.get_user_account(user).debit(
            amount,
            self.account_manager.get_revenue_account(),
            msg)

    @check_thresholds
    def grant_user_promotion(self, user, amount, message):
        account = self.account_manager.get_user_account(user)
        account.credit(
            amount,
            self.account_manager.get_promotions_account(),
            message)
        Notifications.get_notification_sender('promotion_granted').add(
            project_id=user,
            promotion_amount=amount,
            new_balance=account.balance(),
            message=message)
        Notifications.send_all_notifications()


class TransactionHistory():

    def get_account_transaction_history(
            self, acc_name, paginate=False, coords=None, user_values=False):
        """If paginate is true, coords must contain
           the keys 'begin' and 'end'.
        """

        account = managers.AccountManager().get_account(acc_name)
        if paginate:
            acc_entries = account.entries.all()[coords['begin']:coords['end']]
        else:
            acc_entries = account.entries.all()
        return [
            {"tid": x.transaction.tid, "amount": x.amount
             if not (account.positive_credit and user_values)
             else x.amount * -1,
             "timestamp": x.transaction.t_stamp,
             "description": x.transaction.description
             } for x in acc_entries]

    def get_user_account_transaction_history(self, account, **kwargs):
        return self.get_account_transaction_history(
            managers.AccountManager().format_user_account(account),
            **kwargs)
