from horizon import exceptions
from horizon import forms
from resource_pricing.calculators.models import InstanceType
from resource_pricing.models import Price


class UpdatePriceForm(forms.SelfHandlingForm):
    resource_price_id = forms.IntegerField(
        label='resource_price_id', widget=forms.HiddenInput)
    instance_type = forms.CharField(label='instance_type')
    price = forms.DecimalField(label='price')

    def __init__(self, request, *args, **kwargs):
        super(UpdatePriceForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
            instance_type = InstanceType.objects.get(
                resourcebase_ptr=data['resource_price_id'])
            instance_type.os_instance_type_id = data['instance_type']
            instance_type.save()
            price = Price.objects.get(
                resource=instance_type.resourcebase_ptr)
            price.price = data['price']
            price.save()
        except Exception:
            exceptions.handle(request, u'failed to update object')
        return True
