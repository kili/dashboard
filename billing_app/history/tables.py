from horizon import tables
from django.utils.translation import ugettext_lazy as _


class PaymentsHistoryTable(tables.DataTable):
    name = tables.Column("Date",
                         verbose_name=_("Transaction Date"),
                         attrs={'data-type': "date", 'width': "200"},
                         sortable=True,
                         )
    description = tables.Column("Description")
    amount = tables.Column("Amount",
                           verbose_name=_("Transaction Amount"),
                           attrs={'width': "200"},
                           )

    class Meta:
        name = "PayHist"
        verbose_name = _("Payment History")
        status_columns = ["status", "task"]
        table_actions = ()
        row_actions = ()
