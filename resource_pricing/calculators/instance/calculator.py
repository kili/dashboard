from django.core import exceptions
from resource_pricing.calculators import base
from resource_pricing.calculators.instance import models as instance_models


class InstancePriceCalculator(base.CalculatorBase):
    type_name = "instance"
    required_params = ['hours', 'flavor']
    optional_params = []

    def _get_unit_price(self, flavor_id):
        try:
            flavor = instance_models.Flavor.objects.get(
                os_flavor_id=flavor_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find flavor {0}".format(flavor_id))
        return self._get_resource_price(flavor.resource_id)

    def get_price(self, params=None):
        self._validate_params(params)
        unit_price = self._get_unit_price(params['flavor'])
        return unit_price * params['hours']
