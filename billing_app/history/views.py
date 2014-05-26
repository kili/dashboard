from horizon import tables
from .tables import PaymentsHistoryTable


class IndexView(tables.DataTableView):
    template_name = 'billing_app/history/index.html'
    table_class = PaymentsHistoryTable

    transactions = []

    def get_data(self):
        return self.transactions
