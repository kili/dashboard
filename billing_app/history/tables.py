from django.utils.translation import ugettext_lazy as _
from horizon import tables
from user_billing import helpers


class PaymentsHistoryTable(tables.DataTable):
    name = tables.Column("Date",
                         verbose_name=_("Date"),
                         attrs={'data-type': "date", 'width': "200"},
                         sortable=True,
                         )
    description = tables.Column("Description")
    amount = tables.Column("Amount",
                           filters=[helpers.FormattingHelpers.price],
                           verbose_name=_("Amount (USD)"),
                           classes=('text-right',),
                           attrs={'width': "200", 'align': "right"},
                           )

    class Meta:
        name = "PayHist"
        verbose_name = _("Payment History")
        table_actions = ()
        row_actions = ()
        template = "billing_app/usage/_totalled_table.html"
