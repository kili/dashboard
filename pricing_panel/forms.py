from horizon import exceptions
from horizon import forms
from resource_pricing.models import Price


class UpdatePriceForm(forms.SelfHandlingForm):
    resource_price_id = forms.IntegerField(
        label='resource_price_id', widget=forms.HiddenInput)
    instance_type = forms.HiddenInput()
    price = forms.DecimalField(label='price')

    def __init__(self, request, *args, **kwargs):
        super(UpdatePriceForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            price = Price.objects.get(id=data['resource_price_id'])
            price.price = data['price']
            price.save()
        except Exception:
            exceptions.handle(request, u'failed to update object')
        return True
