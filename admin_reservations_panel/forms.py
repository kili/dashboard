from billing_app.models import PrePaidReservation
from django import forms as django_forms
from django.utils.translation import ugettext_lazy as _
from horizon import forms as horizon_forms


class CreateReservationForm(horizon_forms.SelfHandlingMixin,
                            django_forms.ModelForm):

    instance_type = horizon_forms.DynamicChoiceField(
        choices=[],
        label=_("Flavor"),
        add_item_link='horizon:admin:flavors:create')

    api_error = horizon_forms.SelfHandlingForm.api_error
    set_warning = horizon_forms.SelfHandlingForm.set_warning

    class Meta:
        model = PrePaidReservation
        fields = '__all__'

    def handle(self, request, data):
        if self.save():
            return True
