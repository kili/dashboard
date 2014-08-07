from accounting.utils import balance
from billing_app.models import AssignedReservation
from billing_app.models import PrePaidReservation
from billing_app.reservations import tables as reservation_tables
from django.core import urlresolvers
from billing_app.reservations import forms as reservation_forms
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tables as horizon_tables
from openstack_dashboard import api


class IndexView(horizon_tables.MultiTableView):
    template_name = 'billing/reservations/index.html'
    table_classes = (
        reservation_tables.PrepaidReservationsTable,
        reservation_tables.ActiveReservationsTable)

    def get_prepaid_reservations_data(self):
        try:
            return [reservation_tables.PrepaidReservationsTableEntry(
                    x.id,
                    api.nova.flavor_get(self.request, x.instance_type).name,
                    x.formatted_hourly_price, x.formatted_upfront_price,
                    x.length)
                    for x in PrePaidReservation.objects.filter(
                    available=True)]
        except Exception:
            exceptions.handle(self.request,
                              'Unable to retrieve available reservations.')
            return []

    def get_active_reservations_data(self):
        try:
            return [reservation_tables.ActiveReservationsTableEntry(
                    x.id,
                    api.nova.flavor_get(self.request,
                        x.prepaid_reservation.instance_type).name,
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
        prepaid_reservation = PrePaidReservation.objects.get(
            pk=self.kwargs['id'])
        context['user_affords_reservation'] = balance(
            self.request) >= prepaid_reservation.upfront_price
        context['reservation_id'] = self.kwargs['id']
        context['price'] = prepaid_reservation.formatted_upfront_price
        return context
