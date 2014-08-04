from admin_reservations_panel import tables as admin_reservation_tables
from admin_reservations_panel import forms as admin_reservation_forms
from billing_app.models import AssignedReservation
from billing_app.models import PrePaidReservation
from billing_app.reservations import tables as reservation_tables
from django.core import urlresolvers
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tables as horizon_tables
from openstack_dashboard import api


class IndexView(horizon_tables.MultiTableView):
    template_name = 'admin/reservations/index.html'
    table_classes = (
        admin_reservation_tables.AdminPrepaidReservationsTable,
        admin_reservation_tables.AdminActiveReservationsTable)

    def get_prepaid_reservations_data(self):
        try:
            return [reservation_tables.PrepaidReservationsTableEntry(
                    x.id,
                    api.nova.flavor_get(self.request, x.instance_type).name,
                    x.formatted_hourly_price, x.formatted_upfront_price,
                    x.length, x.available)
                    for x in
                    PrePaidReservation.objects.filter()]
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
                    x.start, x.end,
                    api.keystone.tenant_get(self.request, x.tenant_id))
                    for x in
                    AssignedReservation.objects.filter()]
        except Exception:
            exceptions.handle(self.request,
                              'Unable to retrieve active reservations.')
            return []


class ReservationsViewBase(horizon_forms.ModalFormView):
    success_url = urlresolvers.reverse_lazy('horizon:admin:reservations:index')


class CreateReservationView(ReservationsViewBase):
    form_class = admin_reservation_forms.CreateReservationForm
    template_name = \
        'admin/reservations/create_reservation.html'

    def get_initial(self):
        flavors = [(x.id, x.name) for x in api.nova.flavor_list(self.request)]
        self.form_class.base_fields['instance_type'].choices = \
            flavors

        return {'instance_type': 0, 'length': 365}
