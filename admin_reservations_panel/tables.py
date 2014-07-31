from billing_app.reservations.tables import *
from billing_app import models
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from horizon import tables as horizon_tables


class CreateReservation(tables.LinkAction):

    name = 'create'
    verbose_name = _('Create Reservation')
    url = 'horizon:admin:reservations:create'
    classes = ('btn-create', 'ajax-modal')
    ajax = True

class ToggleReservation(tables.BatchAction):

    name = 'toggle'
    verbose_name = _('Toggle Reservation')
    action_past = _('Toggled')
    action_present = _('Toggle')
    data_type_singular = _('Reservation')
    data_type_plural = _('Reservations')

    def action(self, request, prepaid_reservation_id):
        reservation = models.PrePaidReservation.objects.get(
            pk=prepaid_reservation_id)
        reservation.available = not reservation.available
        reservation.save() 

class DeleteReservation(tables.DeleteAction):

    name = 'DeleteCard'
    verbose_name = _('Delete Reservation')
    ajax = True
    action_present = _('Delete')
    action_past = _('Deleted Reservation')
    data_type_singular = _('Reservation')
    data_type_plural = _('Reservations')
    classes = ('btn-danger', 'btn-terminate')

    def delete(self, request, prepaid_reservation_id):
        models.PrePaidReservation.objects.get(
            pk=prepaid_reservation_id).delete()


class AdminPrepaidReservationsTable(PrepaidReservationsTable):
    active = horizon_tables.Column('active', verbose_name='Active')

    class Meta:
        name = 'prepaid_reservations'
        verbose_name = 'Prepaid Reservations'
        table_actions = (CreateReservation, ToggleReservation, DeleteReservation)
        row_actions = (ToggleReservation, DeleteReservation)
    

class AdminActiveReservationsTable(ActiveReservationsTable):
   
    tenant_id = tables.Column(
        'tenant_id', verbose_name='Tenant ID')

    tenant_name = tables.Column(
        'tenant_name', verbose_name='Tenant Name')

    class Meta:
        name = 'active_reservations'
        verbose_name = 'Active Reservations'
        #row_actions = (ExtendReservation,)
