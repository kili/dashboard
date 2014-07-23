from billing_app.context_processors import balance
from billing_app.models import AssignedReservation
from billing_app.models import PrePaidReservation
from datetime import datetime
from datetime import timedelta
from django import forms as django_forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from horizon import forms as horizon_forms


class PurchaseReservationForm(horizon_forms.SelfHandlingForm):

    prepaid_reservation_id = \
        django_forms.IntegerField(widget=django_forms.HiddenInput())

    def handle(self, request, data): 
       try:
            if not self.is_valid():
                raise django_forms.ValidationError('form aint valid') #fix this

            prepaid_reservation = PrePaidReservation.objects.get(
                pk=data['prepaid_reservation_id'])

            if prepaid_reservation.total_price > balance(request)['balance']:
                raise django_forms.ValidationError((
                    'You have insufficient Balance'
                    ' to purchase this reservation')) #redirect maybe?

            ut.consume_user_money(
                request.user.tenant_id,
                prepaid_reservation.total_price,
                u'Purchased {} reservation for {} days'.format(
                    prepaid_reservation.name, prepaid_reservation.length))

            assigned_reservation = AssignedReservation.objects.create(
                tenant_id = request.user.tenant_id,
                start = datetime.now(), 
                end = datetime.now()+timedelta(
                    days=prepaid_reservation.length),
                prepaid_reservation = prepaid_reservation.id)
            
            assigned_reservation.save()

            return True
       except ObjectDoesNotExist:
            self.api_error(u'Invalid Reservation')
       except IntegrityError as e:
            self.api_error(e.message)
       except django_forms.ValidationError as e:
            self.api_error(e.messages[0])
       except Exception:
            exceptions.handle(request, ignore=True)
 
