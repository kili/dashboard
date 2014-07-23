from billing_app.models import PrePaidReservation
from django import forms as django_forms
from django.utils.translation import ugettext_lazy as _
from horizon import forms as horizon_forms
from django.db import IntegrityError


class CreateReservationForm(horizon_forms.SelfHandlingMixin,
                            django_forms.ModelForm):

    instance_type = horizon_forms.DynamicChoiceField(
        choices=[],
        label=_("Flavor"),
        add_item_link='')
    
    hourly_price = django_forms.DecimalField(
        max_digits=5, decimal_places=2)

    total_price = django_forms.DecimalField(
        max_digits=5, decimal_places=2)
    
    length = django_forms.IntegerField(
        label=_("Length in Days"))

    api_error = horizon_forms.SelfHandlingForm.api_error
    set_warning = horizon_forms.SelfHandlingForm.set_warning

    class Meta:
        model = PrePaidReservation
        fields = '__all__'

    def handle(self, request, data):
        try:
            if not self.is_valid():
                raise django_forms.ValidationError('form aint valid') #fix this
            self.save()
            return True
        except IntegrityError as e:
            self.api_error(e.message)
        except django_forms.ValidationError as e:
            self.api_error(e.messages[0])
        except Exception:
            exceptions.handle(request, ignore=True)
