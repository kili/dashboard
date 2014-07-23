from admin_reservations_panel import tables as admin_reservation_tables
from admin_reservations_panel import forms as admin_reservation_forms
from billing_app.models import AssignedReservation
from billing_app.models import PrePaidReservation
from django.core import urlresolvers
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tables as horizon_tables
from horizon import views
from openstack_dashboard import api


class PrepaidReservationsTableEntry(object):

    def __init__(self, id, instance_type, hourly_price,
                 total_price, length, active):
        self.id = id
        self.instance_type = instance_type
        self.hourly_price = hourly_price
        self.total_price = total_price
        self.length = length
        self.active = active 
 
    @property
    def name(self):
        return instance_type 

class ActiveReservationsTableEntry(object):

    def __init__(self, id, instance_type, start, end):
        self.id = id
        self.instance_type = instance_type
        self.start = start
        self.end = end

    @property
    def name(self):
        return instance_type 

class IndexView(horizon_tables.MultiTableView):
    template_name = 'admin/reservations/index.html'
    table_classes = (
        admin_reservation_tables.AdminPrepaidReservationsTable,
        admin_reservation_tables.AdminActiveReservationsTable)

    def get_prepaid_reservations_data(self):
        try:
            return [PrepaidReservationsTableEntry(x.id, 
                    api.nova.flavor_get(self.request, x.instance_type).name,
                    x.hourly_price, x.total_price, x.length, x.available)
                    for x in PrePaidReservation.objects.filter()]
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
        flavors = api.nova.flavor_list(self.request)
        flavor_choices = []

        for flavor in flavors:
            flavor_choices.append((flavor.id, flavor.name))

        self.form_class.base_fields['instance_type'].choices = \
            flavor_choices;

        return {'instance_type': 0,
                'hourly_price': 0,
                'total_price': 0,
                'length': 0}
