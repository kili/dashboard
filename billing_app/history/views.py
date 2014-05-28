from billing_app.history import tables as billing_tables
from horizon import tables as horizon_tables


class IndexView(horizon_tables.DataTableView):
    template_name = 'billing_app/history/index.html'
    table_class = billing_tables.PaymentsHistoryTable

    def get_1_data(self):
        transactions = []
        return transactions

    def get_2_data(self):
        transactions = []
        return transactions
