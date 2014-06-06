from django.core import exceptions
from resource_pricing.calculators import base
from resource_pricing.calculators.volume import models as volume_models


class VolumePriceCalculator(base.CalculatorBase):
    type_name = "volume"
    required_params = ['hours', 'gb_size', 'type']
    optional_params = []

    def __init__(self):
        super(VolumePriceCalculator, self).__init__()

    def _get_unit_price(self, vtype_id):
        try:
            volume_type = volume_models.VolumeType.objects.get(
                os_type_id=vtype_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find volume type {0}".format(vtype_id))
        return self._get_resource_price(volume_type.resource_id)

    def get_price(self, params=None):
        self._validate_params(params)
        unit_price = self._get_unit_price(params['type'])
        return unit_price * params['gb_size'] * params['hours']
