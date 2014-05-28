from horizon import tables
from .tables import PaymentsHistoryTable


class IndexView(tables.DataTableView):
    template_name = 'billing_app/history/index.html'
    table_class = PaymentsHistoryTable

    def get_1_data(self):
        transactions = []
        return transactions

    def get_2_data(self):
        transactions = []
        return transactions
