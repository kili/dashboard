from django.utils.translation import ugettext_lazy as _
from horizon import tables


class UsageTable(tables.DataTable):
    resource = tables.Column("resource",
                             verbose_name="Resource",
                             sortable=True)
    hours = tables.Column("hours",
                          verbose_name="Hours")
    price = tables.Column("price",
                          verbose_name="Price",
                          sortable=True)

    class Meta:
        name = "usage"
        verbose_name = "Resource Usage"
        table_actions = ()
        row_actions = ()
