from django.core import exceptions
from resource_pricing.calculators import base
from resource_pricing.calculators.instance import models as instance_models
from resource_pricing import models as resource_price_models


class InstancePriceCalculator(base.CalculatorBase):
    type_name = "instance"
    required_params = ['hours', 'flavor']
    optional_params = []

    def __init__(self):
        if not self._type_is_configured():
            raise Exception("the type {0} is not configured".format(
                self.type_name))

    def _get_unit_price(self, flavor_id):
        try:
            flavor = instance_models.Flavor.objects.get(
                os_flavor_id=flavor_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find flavor {0}".format(flavor_id))
        try:
            resource = resource_price_models.ResourcePrice.objects.get(
                resource_id=flavor.resource_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find resource_id {0}"
                            .format(flavor.resource_id))
        return resource.price

    def get_price(self, params=None):
        self._validate_params(params)
        unit_price = self._get_unit_price(params['flavor'])
        return unit_price * params['hours']
