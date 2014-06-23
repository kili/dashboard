from horizon import exceptions
from horizon import forms
from resource_pricing.calculators import models as calc_models
from resource_pricing import models as pricing_models


class UpdatePriceForm(forms.SelfHandlingForm):
    resource_price_id = forms.IntegerField(
        label='resource_price_id', widget=forms.HiddenInput)
    flavor = forms.CharField(label='flavor')
    price = forms.DecimalField(label='price')

    def __init__(self, request, *args, **kwargs):
        super(UpdatePriceForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            flavor = calc_models.Flavor.objects.get(
                resource=data['resource_price_id'])
            flavor.os_flavor_id = data['flavor']
            flavor.save()
            price = pricing_models.Price.objects.get(resource=flavor.resource)
            price.price = data['price']
            price.save()
        except Exception:
            exceptions.handle(request, u'failed to update object')
        return True
