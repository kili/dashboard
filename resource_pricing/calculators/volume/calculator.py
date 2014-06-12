import decimal
from resource_pricing.calculators import base


class PriceCalculator(base.VolumeAndInstancePriceCalculatorBase):
    type_name = "volume"
    required_params = ['hours', 'gb_size', 'type']
    optional_params = []
    resource_type_relation = "resource__volumetype__os_type_id"
    type_key = "type"

    def __init__(self):
        super(PriceCalculator, self).__init__()

    def _specific_param_checks(self, params):
        super(PriceCalculator, self)._specific_param_checks(params)
        if decimal.Decimal(params['gb_size']) < decimal.Decimal(1.0):
            raise Exception('the given gb_size cannot be less than 1')

    def _final_calculation(self, params):
        return (self._get_unit_price(params['type']) *
                decimal.Decimal(params['gb_size']) *
                decimal.Decimal(params['hours']))

    def _get_params_from_raw_stats(self, meter, raw_data):
        return {
            'hours': decimal.Decimal(raw_data['count'] *
                                     self.type_settings['period_length']
                                     ) / 60,
            'gb_size': raw_data['gb_size'],
            'type': meter}
