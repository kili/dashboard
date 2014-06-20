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

    def _specific_param_checks(self, params):
        pass

    def _get_params_from_raw_stats(self, *args, **kwargs):
        raise NotImplemented

    def get_hours_from_periods(self, periods):
        return (decimal.Decimal(self.type_settings['period_length']) *
                decimal.Decimal(periods) / decimal.Decimal(60))

    def get_typed_object_by_id(self, id):
        return self._get_typed_object_by_id(id)

    def get_typed_object_by_name(self, name):
        return self._get_typed_object_by_name(name)

    def get_all_prices(self):
        return self._get_all_prices()

    def price_from_raw_stats(self, raw_data):
        params = self._get_params_from_raw_stats(raw_data)
        self._validate_params(params)
        return {'price': self._final_calculation(params),
                'hours': params['hours'],
                'res_string': params['res_string']}


class VolumeAndInstancePriceCalculatorBase(CalculatorBase):

    def __init__(self):
        super(VolumeAndInstancePriceCalculatorBase, self).__init__()

    def _get_unit_by_name(self, type_id, currency="USD"):
        return self._get_unit(type_id, self.resource_type_relation, currency)

    def _get_unit_by_id(self, id, currency="USD"):
        return self._get_unit(id, self.resource_id_relation, currency)

    def _get_unit(self, id, selector, currency="USD"):
        try:
            unit = models.Price.objects.get(
                **{"currency__iso": currency,
                   selector: id})
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not get price of id {0} in currency "
                            "{1}".format(id, currency))
        return unit

    def _get_typed_object_by_id(self, id, currency='USD'):
        return self._get_typed_object(id,
                                      self.resource_id_relation,
                                      currency)

    def _get_typed_object_by_name(self, name, currency='USD'):
        return self._get_typed_object(name,
                                      self.resource_type_relation,
                                      currency)

    def _get_typed_object(self, key, selector, currency='USD'):
        return self._get_model().objects.get(**{selector: key})

    def _get_unit_price(self, type_id, currency="USD"):
        return self._get_unit_by_name(type_id, currency).price

    def _get_all_prices(self, currency="USD"):
        return [{'resource_id': x.resource.id,
                 'description': x.resource.description,
                 'price': x.price} for x in
                 models.Price.objects.exclude(
                     resource__flavor__os_flavor_id=None)]

    def _specific_param_checks(self, params):
        if params['hours'] < 0:
            raise Exception('the consumed hours cannot be less than 0')

    def _get_resource_price_info(self, resource_id):
        pass
