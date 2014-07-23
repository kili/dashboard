from billing_app.context_processors import balance
from billing_app.models import AssignedReservation
from billing_app.models import PrePaidReservation
from billing_app.reservations import tables as reservation_tables
from django.core import urlresolvers
from billing_app.reservations import forms as reservation_forms
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tables as horizon_tables
from horizon import views
from openstack_dashboard import api


class PrepaidReservationsTableEntry(object):

    def __init__(self, id, instance_type, hourly_price,
                 total_price, length):
        self.id = id
        self.instance_type = instance_type
        self.hourly_price = hourly_price
        self.total_price = total_price
        self.length = length

    @property
    def name(self):
        return instance_type 

class ActiveReservationsTableEntry(object):

    def __init__(self, instance_type, name, start, end):
        self.id = id
        self.instance_type = instance_type
        self.start = start
        self.end = end

    @property
    def name(self):
        return instance_type 

class IndexView(horizon_tables.MultiTableView):
    template_name = 'billing/reservations/index.html'
    table_classes = (
        reservation_tables.PrepaidReservationsTable,
        reservation_tables.ActiveReservationsTable)


    def get_prepaid_reservations_data(self):
        try:
            return [PrepaidReservationsTableEntry(
                    x.id, 
                    api.nova.flavor_get(self.request, x.instance_type).name,
                    x.hourly_price, x.total_price, x.length)
                    for x in PrePaidReservation.objects.filter(
                    available=True)]
        except Exception:
            exceptions.handle(self.request,
                 'Unable to retrieve available reservations.')
            return []

    def get_active_reservations_data(self):
        try:
            return [ActiveReservationsTableEntry(
                    x.id, 
                    api.nova.flavor_get(self.request, x.instance_type).name,
                    x.start, x.end)
                    for x in AssignedReservation.objects.filter(
                    tenant_id__exact=self.request.user.tenant_id)]
        except Exception:
            exceptions.handle(self.request,
                 'Unable to retrieve active reservations.')
            return []

class ReservationsViewBase(horizon_forms.ModalFormView):
    success_url = urlresolvers.reverse_lazy(
        'horizon:billing:reservations:index')

class PurchaseView(ReservationsViewBase):
    form_class = reservation_forms.PurchaseReservationForm
    template_name = 'billing/reservations/purchase_reservation.html'
        
    def get_context_data(self, **kwargs):
        context = super(PurchaseView, self).get_context_data(**kwargs)
        if self.request.GET and self.request.GET.get('PrePaidReservation'):
            prepaid_reservation = PrePaidReservation.objects.get(
                pk=self.request.GET['PrePaidReservation'])

            affordable = prepaid_reservation.total_price > balance(
                self.request)['balance']

            context['submit_url'] = 'horizon:billing:reservation:purchase'\
                if affordable else 'horizon:billing:payments:index'

            context['modal_message'] = \
                'Are you sure you want to purchase this reservation?'\
                if affordable else ('You have insufficient funds for this this'
                   ' reservation Would you like to top up your account?')
        return context
