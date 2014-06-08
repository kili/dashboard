import decimal
from resource_pricing.calculators import base


class VolumePriceCalculator(base.VolumeAndInstancePriceCalculatorBase):
    type_name = "volume"
    required_params = ['hours', 'gb_size', 'type']
    optional_params = []
    resource_type_relation = "resource__volumetype__os_type_id"
    type_key = "type"

    def __init__(self):
        super(VolumePriceCalculator, self).__init__()

    def _specific_param_checks(self, params):
        super(VolumePriceCalculator, self)._specific_param_checks(params)
        if decimal.Decimal(params['gb_size']) < decimal.Decimal(1.0):
            raise Exception('the given gb_size cannot be less than 1')

    def _final_calculation(self, params, unit_price):
        return (unit_price *
                decimal.Decimal(params['gb_size']) *
                decimal.Decimal(params['hours']))
