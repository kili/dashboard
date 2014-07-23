from billing_app.reservations import tables as user_reservation_tables
from billing_app import models
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from horizon import tables as horizon_tables


class CreateReservation(horizon_tables.LinkAction):

    name = 'create'
    verbose_name = _('Create Reservation')
    url = 'horizon:admin:reservations:create'
    classes = ('btn-create', 'ajax-modal')
    ajax = True

class ToggleReservation(horizon_tables.BatchAction):

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

class DeleteReservation(horizon_tables.DeleteAction):

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


class AdminPrepaidReservationsTable(user_reservation_tables.PrepaidReservationsTable):
    active = horizon_tables.Column('active', verbose_name='Active')

    class Meta:
        name = 'prepaid_reservations'
        verbose_name = 'Prepaid Reservations'
        table_actions = (CreateReservation, ToggleReservation, DeleteReservation)
        row_actions = (ToggleReservation, DeleteReservation)
    

class AdminActiveReservationsTable(user_reservation_tables.ActiveReservationsTable):
    
    class Meta:
        name = 'active_reservations'
        verbose_name = 'Active Reservations'
        #row_actions = (ExtendReservation,)
