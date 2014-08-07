from accounting import transactions
from billing_app.history import tables as history_tables
from horizon import tables as horizon_tables


class IndexView(horizon_tables.DataTableView):
    template_name = 'billing/history/index.html'
    table_class = history_tables.TransactionHistoryTable

    def get_context_data(self, **kwargs):
        return dict(super(IndexView, self).get_context_data(**kwargs).items() +
                    [('project', self.request.user.tenant_name)])

    def get_data(self):
        return [history_tables.TransactionHistoryTableEntry(
            x['tid'],
            x['timestamp'],
            x['description'],
            x['amount']) for x in transactions.TransactionHistory().
            get_user_account_transaction_history(
                self.request.user.tenant_id, user_values=True)]
