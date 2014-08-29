from django.core import urlresolvers
from horizon import forms
from horizon import tables as horizon_tables
from nova_wrapper.client import NovaClient
from pricing_panel import forms as pricing_forms
from pricing_panel import tables
from resource_pricing.calculators.models import InstanceType
from resource_pricing.models import Price


class IndexView(horizon_tables.MultiTableView):
    table_classes = (tables.InstancePricesTable,)
    template_name = 'admin/pricing/index.html'

    def get_instance_prices_data(self):
        return [tables.InstancePricesTableEntry(
            id=x.resource.id,
            instance_type=NovaClient.instance_type_id_to_name(
                x.resource.instancetype.os_instance_type_id),
            price=x.price)
            for x in Price.objects.exclude(
                resource__instancetype__os_instance_type_id=None)]


class UpdateView(forms.ModalFormView):
    form_class = pricing_forms.UpdatePriceForm
    template_name = 'admin/pricing/update.html'
    success_url = urlresolvers.reverse_lazy('horizon:admin:pricing:index')

    def get_object(self):
        instance_type = InstanceType.objects.get(
            resourcebase_ptr=self.kwargs['resource_price_id'])
        price = Price.objects.get(resource=instance_type.resourcebase_ptr)
        return {'resource_price_id': self.kwargs['resource_price_id'],
                'instance_type': instance_type.os_instance_type_id,
                'price': price.price}

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['price'] = self.get_object()
        return context

    def get_initial(self):
        price = self.get_object()
        return price
