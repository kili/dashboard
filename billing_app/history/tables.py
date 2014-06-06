from django.utils.translation import ugettext_lazy as _
from horizon import tables


class PaymentsHistoryTable(tables.DataTable):
    name = tables.Column("Date",
                         verbose_name=_("Transaction Date"),
                         attrs={'data-type': "date", 'width': "200"},
                         sortable=True,
                         )
    description = tables.Column("Description")
    amount = tables.Column("Amount",
                           verbose_name=_("Transaction Amount"),
                           attrs={'width': "200", 'align': "right"},
                           )

    class Meta:
        name = "PayHist"
        verbose_name = _("Payment History")
        table_actions = ()
        row_actions = ()
