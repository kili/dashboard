import decimal
from resource_pricing.calculators import base


class InstancePriceCalculator(base.VolumeAndInstancePriceCalculatorBase):
    type_name = "instance"
    resource_type_relation = "resource__flavor__os_flavor_id"
    required_params = ['hours', 'flavor']
    optional_params = []
    type_key = "flavor"

    def __init__(self):
        super(InstancePriceCalculator, self).__init__()

    def _final_calculation(self, params, unit_price):
        return unit_price * decimal.Decimal(params['hours'])
