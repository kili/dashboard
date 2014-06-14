import decimal
from horizon import tables


class FormattingHelpers(object):

    @staticmethod
    def price(table_element):
        price = decimal.Decimal(table_element.price).quantize(
            decimal.Decimal('0.00'))
        return "{0}$".format(price)

    @staticmethod
    def hours(table_element):
        hours = table_element.hours.quantize(
            decimal.Decimal('0'))
        mins = (table_element.hours.remainder_near(
            decimal.Decimal('1')) * 60).quantize(
                decimal.Decimal('0'))
        return "{0}:{1:02}".format(hours, mins)


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
    hours = tables.Column(FormattingHelpers.hours,
                          verbose_name='Hours',
                          sortable=True)
    price = tables.Column(FormattingHelpers.price,
                          verbose_name='Price',
                          sortable=True)

    class Meta:
        name = 'instances'
        verbose_name = 'Instances'
        table_actions = ()
        row_actions = ()
