from horizon import tables
from user_billing import helpers


class UpdatePrice(tables.LinkAction):
    name = 'update'
    verbose_name = 'Edit Price'
    url = 'horizon:admin:pricing:update'
    classes = ('ajax-modal', 'btn-edit')


class InstancePricesTableEntry(object):

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.flavor = kwargs['flavor']
        self.price = kwargs['price']


class InstancePricesTable(tables.DataTable):
    flavor = tables.Column('flavor',
                         verbose_name='OS Flavor ID')
    price = tables.Column('price',
                          filters=[helpers.FormattingHelpers.price],
                          verbose_name='Price/h')

    class Meta:
        name = 'instance_prices'
        verbose_name = 'Instance Prices'
        table_actions = ()
        row_actions = (UpdatePrice,)
