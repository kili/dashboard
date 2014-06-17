import decimal
from resource_pricing.calculators import base


class PriceCalculator(base.VolumeAndInstancePriceCalculatorBase):
    type_name = "instance"
    resource_type_relation = "resource__flavor__os_flavor_id"
    required_params = ['hours', 'flavor', 'res_string']
    optional_params = []
    type_key = "flavor"

    def __init__(self):
        super(PriceCalculator, self).__init__()

    def _final_calculation(self, params):
        return (self._get_unit_price(params['flavor']) *
                decimal.Decimal(params['hours']))

    def _get_params_from_raw_stats(self, raw_data):
        return {
            'hours': self.get_hours_from_periods(raw_data[0]['count']),
            'flavor': 'instance:' + raw_data[1]['metadata']['flavor.name'],
            'res_string': 'instance:' + raw_data[1]['metadata']['flavor.name']
            + ':' + raw_data[1]['metadata']['display_name']}
