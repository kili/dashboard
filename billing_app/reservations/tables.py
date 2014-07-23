from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse  # noqa
from horizon import tables
from django.core.urlresolvers import reverse


class PurchaseReservation(tables.LinkAction):

    name = 'purchase'
    verbose_name = 'Purchase Reservation'
    url = 'horizon:billing:reservations:purchase'
    classes = ('btn-success', 'ajax-modal')
    ajax = True

    def get_link_url(self, datum=None):
        return '{}?PrePaidReservation={}'.format(
            reverse('horizon:billing:reservations:purchase'),
            datum.id)
            

class PrepaidReservationsTable(tables.DataTable):

    instance_type = tables.Column(
        'instance_type', verbose_name='Instance Type')
    hourly_price = tables.Column(
        'hourly_price', verbose_name='Price per Hour')
    total_price = tables.Column(
        'total_price', verbose_name='Total Price')
    length = tables.Column(
        'length', verbose_name='Duraion (Days)'),
 
    class Meta:
        name = 'prepaid_reservations'
        verbose_name = 'Prepaid Reservations'
        row_actions = (PurchaseReservation, )


class ExtendReservation(tables.LinkAction):

    name = 'extend'
    verbose_name = 'Extend Reservation'
    url = 'horizon:billing:reservations:extend_reservation'
    classes = ('btn-success', 'ajax-modal')
    ajax = True


class ActiveReservationsTable(tables.DataTable):

    instance_type = tables.Column(
        'type', verbose_name='Instance_type')
    start = tables.Column(
        'start', verbose_name='Created')
    end = tables.Column(
        'end', verbose_name='Expires')
   
    class Meta:
        name = 'active_reservations'
        verbose_name = 'Active Reservations'
        row_actions = (ExtendReservation,)
