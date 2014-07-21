from horizon import tables
from project_billing import helpers


class UpdatePriceAction(tables.LinkAction):
    name = 'update'
    verbose_name = 'Edit Price'
    url = 'horizon:admin:pricing:update'
    classes = ('ajax-modal', 'btn-edit')


class InstancePricesTableEntry(object):

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.instance_type = kwargs['instance_type']
        self.price = kwargs['price']


class InstancePricesTable(tables.DataTable):
    instance_type = tables.Column('instance_type',
                         verbose_name='OS Instance Type ID')
    price = tables.Column('price',
                          filters=[helpers.FormattingHelpers.price],
                          verbose_name='Price/h')

    class Meta:
        name = 'instance_prices'
        verbose_name = 'Instance Prices'
        table_actions = ()
        row_actions = (UpdatePriceAction,)
