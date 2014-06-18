from horizon import tables
from user_billing import helpers


class InstanceUsageTableEntry(object):

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.flavor = kwargs['flavor']
        self.hours = kwargs['hours']
        self.price = kwargs['price']


class InstanceUsageTable(tables.DataTable):
    name = tables.Column('name',
                         verbose_name='Name',
                         sortable=True)
    flavor = tables.Column('flavor',
                           verbose_name='Flavor',
                           sortable=True)
    hours = tables.Column('hours',
                          filters=[helpers.FormattingHelpers.hours],
                          verbose_name='Hours',
                          sortable=True,
                          summation='sum')
    price = tables.Column('price',
                          filters=[helpers.FormattingHelpers.price],
                          verbose_name='Price',
                          sortable=True,
                          summation='sum')

    class Meta:
        name = 'instances'
        verbose_name = 'Instances'
        table_actions = ()
        row_actions = ()
        template = "billing_app/usage/_totalled_table.html"
