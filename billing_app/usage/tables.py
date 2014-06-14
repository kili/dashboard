from horizon import tables


class InstanceUsageTableEntry():

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
                          verbose_name='Hours',
                          sortable=True)
    price = tables.Column('price',
                          verbose_name='Price',
                          sortable=True)

    class Meta:
        name = 'instances'
        verbose_name = 'Instances'
        table_actions = ()
        row_actions = ()
