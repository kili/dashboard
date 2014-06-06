from django.core import exceptions
from resource_pricing.calculators import base
from resource_pricing.calculators.volume import models as volume_models
from resource_pricing import models as resource_price_models


class VolumePriceCalculator(base.CalculatorBase):
    type_name = "volume"
    required_params = ['hours', 'gb_size', 'type']
    optional_params = []

    def __init__(self):
        if not self._type_is_configured():
            raise Exception("the type {0} is not configured".format(
                self.type_name))

    def _get_unit_price(self, vtype_id):
        try:
            volume_type = volume_models.VolumeType.objects.get(
                os_type_id=vtype_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find volume type {0}".format(vtype_id))
        try:
            resource = resource_price_models.ResourcePrice.objects.get(
                resource_id=volume_type.resource_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find resource_id {0}"
                            .format(volume_type.resource_id))
        return resource.price

    def get_price(self, params=None):
        self._validate_params(params)
        unit_price = self._get_unit_price(params['type'])
        return unit_price * params['gb_size'] * params['hours']
