from django.utils.translation import ugettext_lazy as _
from horizon import tables
from project_billing import helpers


class TransactionHistoryTableEntry():

    def __init__(self, id, Date, Description, Amount):
        self.id = id
        self.Date = Date
        self.Description = Description
        self.Amount = Amount


class TransactionHistoryTable(tables.DataTable):
    name = tables.Column("Date",
                         verbose_name=_("Date"),
                         attrs={'data-type': "date", 'width': "200"},
                         sortable=True)
    description = tables.Column("Description")
    amount = tables.Column("Amount",
                           filters=[helpers.FormattingHelpers.price],
                           verbose_name=_("Amount (USD)"),
                           classes=('text-right',),
                           attrs={'width': "200", 'align': "right"},
                           summation='sum')

    class Meta:
        name = "TransHist"
        verbose_name = _("Transactions")
        table_actions = ()
        row_actions = ()
