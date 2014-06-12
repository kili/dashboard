import decimal
from django.conf import settings
from resource_pricing.calculators import base


class PriceCalculator(base.VolumeAndInstancePriceCalculatorBase):
    type_name = "instance"
    resource_type_relation = "resource__flavor__os_flavor_id"
    required_params = ['hours', 'flavor']
    optional_params = []
    type_key = "flavor"

    def __init__(self):
        super(PriceCalculator, self).__init__()

    def _final_calculation(self, params):
        return (self._get_unit_price(params['flavor']) *
                decimal.Decimal(params['hours']))

    def _get_params_from_raw_stats(self, meter, raw_data):
        return {
            'hours': (decimal.Decimal(raw_data['count'] *
                                      settings.CEILOMETER_NOVA_PERIOD_LENGTH
                                      ) / 60),
            'flavor': meter}
