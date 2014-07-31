from billing_app.context_processors import balance
from billing_app.models import AssignedReservation
from billing_app.models import PrePaidReservation
from datetime import datetime
from datetime import timedelta
from django import forms as django_forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from horizon import forms as horizon_forms
from accounting.transactions import UserTransactions 
from openstack_dashboard import api


class PurchaseReservationForm(horizon_forms.SelfHandlingForm):

    prepaid_reservation_id = \
        django_forms.IntegerField(widget=django_forms.HiddenInput())

    def handle(self, request, data): 
       try:
            if not self.is_valid():
                raise django_forms.ValidationError('form aint valid') #fix this

            prepaid_reservation = PrePaidReservation.objects.get(
                pk=data['prepaid_reservation_id'])

            if prepaid_reservation.upfront_price > balance(request)['balance']:
                raise django_forms.ValidationError((
                    'You have insufficient Balance'
                    ' to purchase this reservation')) #redirect maybe?
            UserTransactions().consume_user_money(
                request.user.tenant_id,
                prepaid_reservation.upfront_price,
                u'Purchased {} reservation for {} days'.format(
                    api.nova.flavor_get(request, 
                        prepaid_reservation.instance_type),
                    prepaid_reservation.length))

            assigned_reservation = AssignedReservation.objects.create(
                tenant_id = request.user.tenant_id,
                start = datetime.now(), 
                end = datetime.now()+timedelta(
                    days=prepaid_reservation.length),
                prepaid_reservation = prepaid_reservation)
            
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
 
