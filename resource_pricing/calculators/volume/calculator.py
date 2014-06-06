from resource_pricing.calculators import base


class VolumePriceCalculator(base.VolumeAndInstancePriceCalculatorBase):
    type_name = "volume"
    required_params = ['hours', 'gb_size', 'type']
    optional_params = []
    resource_type_relation = "resource__volumetype__os_type_id"
    type_key = "type"

    def __init__(self):
        super(VolumePriceCalculator, self).__init__()

    def _final_calculation(self, params, unit_price):
        return unit_price * params['gb_size'] * params['hours']
