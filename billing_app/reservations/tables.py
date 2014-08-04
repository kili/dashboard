from django.http import HttpResponse  # noqa
from horizon import tables


class PurchaseReservation(tables.LinkAction):

    name = 'purchase'
    verbose_name = 'Purchase'
    url = 'horizon:billing:reservations:purchase'
    classes = ('btn-success', 'ajax-modal')
    ajax = True


class PrepaidReservationsTableEntry(object):

    def __init__(self, id, instance_type, hourly_price,
                 upfront_price, length, active=True):
        self.id = id
        self.instance_type = instance_type
        self.hourly_price = hourly_price
        self.upfront_price = upfront_price
        self.length = length
        self.active = active

    @property
    def name(self):
        return self.instance_type


class PrepaidReservationsTable(tables.DataTable):

    instance_type = tables.Column(
        'instance_type', verbose_name='Instance Type')
    hourly_price = tables.Column(
        'hourly_price', verbose_name='Price per Hour')
    upfront_price = tables.Column(
        'upfront_price', verbose_name='Upfront Price')
    length = tables.Column(
        'length', verbose_name='Duration (Days)'),

    class Meta:
        name = 'prepaid_reservations'
        verbose_name = 'Available Reservations'
        row_actions = (PurchaseReservation, )


class ActiveReservationsTableEntry(object):

    def __init__(self, id, instance_type,
                 start, end, tenant=None):
        self.id = id
        self.instance_type = instance_type
        self.start = start
        self.end = end
        if tenant:
            self.tenant_id = tenant.id
            self.tenant_name = tenant.name

    @property
    def name(self):
        return self.instance_type


class ActiveReservationsTable(tables.DataTable):

    instance_type = tables.Column(
        'instance_type', verbose_name='Instance Type')
    start = tables.Column(
        'start', verbose_name='Created')
    end = tables.Column(
        'end', verbose_name='Expires')

    class Meta:
        name = 'active_reservations'
        verbose_name = 'Active Reservations'
