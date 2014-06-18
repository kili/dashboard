import decimal
from django.conf import settings
from django.core import exceptions
from resource_pricing import models
from resource_pricing import types


class CalculatorBase(object):
    type_settings = None
    optional_params = []
    required_params = []
    types = types.ResourceTypes()
    type_name = None

    def __init__(self):
        if not self._type_is_configured():
            raise Exception("the type {0} is not configured".format(
                self.type_name))

    def _type_is_configured(self):
        if self.type_name in settings.BILLABLE_RESOURCE_TYPES.keys():
            self.type_settings = settings.BILLABLE_RESOURCE_TYPES[
                self.type_name]
            return True
        return False

    def _validate_params(self, params):
        for x in self.required_params:
            if x not in params:
                raise Exception("the required parameter {0} is missing".
                                format(x))
        for x in params.keys():
            if (x not in self.optional_params and
                    x not in self.required_params):
                raise Exception("the given parameter {0} is unknown".
                                format(x))
        self._specific_param_checks(params)

    def _get_resource_price(self, resource_id, currency="USD"):
        try:
            price = models.Price.objects.get(currency__iso=currency,
                                             resource=resource_id)
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not find price for resource {0} with"
                            " currency {1}".format(resource_id, currency))
        return price.price

    def _specific_param_checks(self, params):
        pass

    def _get_params_from_raw_stats(self, *args, **kwargs):
        raise NotImplemented

    def get_hours_from_periods(self, periods):
        return (decimal.Decimal(self.type_settings['period_length']) *
                decimal.Decimal(periods) / decimal.Decimal(60))

    def price_from_raw_stats(self, raw_data):
        params = self._get_params_from_raw_stats(raw_data)
        self._validate_params(params)
        return {'price': self._final_calculation(params),
                'hours': params['hours'],
                'res_string': params['res_string']}


class VolumeAndInstancePriceCalculatorBase(CalculatorBase):

    def __init__(self):
        super(VolumeAndInstancePriceCalculatorBase, self).__init__()

    def _get_unit_price(self, type_id, currency="USD"):
        try:
            price = models.Price.objects.get(
                **{"currency__iso": currency,
                   self.resource_type_relation: type_id})
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not get price of type {0} in currency "
                            "{1}".format(type_id, currency))
        return price.price

    def _specific_param_checks(self, params):
        if params['hours'] < 0:
            raise Exception('the consumed hours cannot be less than 0')
