from accounting import transactions
from billing_app.history import tables as billing_tables
from horizon import tables as horizon_tables


class TransactionHistoryTableEntry():

    def __init__(self, id, Date, Description, Amount):
        self.id = id
        self.Date = Date
        self.Description = Description
        self.Amount = Amount


class IndexView(horizon_tables.DataTableView):
    template_name = 'billing_app/history/index.html'
    table_class = billing_tables.PaymentsHistoryTable

    def get_data(self):
        return [TransactionHistoryTableEntry(
            x['tid'],
            x['timestamp'],
            x['description'],
            x['amount']) for x in transactions.TransactionHistory().\
            get_user_account_transaction_history(
                self.request.user.id, user_values=True)]
