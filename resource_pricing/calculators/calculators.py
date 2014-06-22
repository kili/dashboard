import abc
import decimal
from django.conf import settings
from django.core import exceptions
import importlib
from resource_pricing.calculators import models
from resource_pricing import models as pricing_models


class CalculatorBase(object):
    __metaclass__ = abc.ABCMeta
    optional_params = []
    required_params = []

    def __init__(self):
        if self.type_name not in settings.BILLABLE_RESOURCE_TYPES.keys():
            raise Exception("the type {0} is not configured".format(
                self.type_name))
        self.type_settings = settings.BILLABLE_RESOURCE_TYPES[self.type_name]

    @abc.abstractmethod
    def _final_calculation(self, params):
        """do the type specific calculations."""
        return

    @abc.abstractmethod
    def _get_model(self, params):
        """return the model where data about this resource type are stored."""
        return

    @abc.abstractmethod
    def _get_params_from_raw_stats(self, raw_data):
        """extract the datapoints which are required to do price calculations
           from raw statistics.
        """
        return

    @abc.abstractproperty
    def resource_type_relation(self):
        pass

    @abc.abstractproperty
    def type_key(self):
        pass

    @abc.abstractproperty
    def type_name(self):
        pass

    def _get_unit_price(self, type_id, currency="USD"):
        try:
            return pricing_models.Price.objects.get(
                **{"currency__iso": currency,
                   self.resource_type_relation: type_id}).price
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not get price of id {0} in currency "
                            "{1}".format(id, currency))

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
        if params['hours'] < 0:
            raise Exception('the consumed hours cannot be less than 0')

    def get_hours_from_periods(self, periods):
        return (decimal.Decimal(self.type_settings['period_length']) *
                decimal.Decimal(periods) / decimal.Decimal(60))

    @classmethod
    def get_price_calculator_of_meter(self, meter):
        brt = settings.BILLABLE_RESOURCE_TYPES
        pc_name = ''
        for k, v in brt.items():
            if k == meter:
                pc_name = v['price_calculator']
                break
        if pc_name == '':
            raise Exception('price calculator for {0} not configured'.format(
                meter))
        bits = pc_name.split('.')
        return getattr(
            importlib.import_module('.'.join(bits[:-1])), bits[-1])()

    def price_from_raw_stats(self, raw_data):
        params = self._get_params_from_raw_stats(raw_data)
        self._validate_params(params)
        return {'price': self._final_calculation(params),
                'hours': params['hours'],
                'res_string': params['res_string']}


class VolumePriceCalculator(CalculatorBase):
    type_name = "volume"
    required_params = ['hours', 'gb_size', 'type', 'res_string']
    optional_params = []
    resource_type_relation = "resource__volumetype__os_type_id"
    type_key = "type"

    def _final_calculation(self, params):
        return (self._get_unit_price(params['type']) *
                decimal.Decimal(params['gb_size']) *
                decimal.Decimal(params['hours']))

    def _get_model(self):
        return models.VolumeType

    def _get_params_from_raw_stats(self, raw_data):
        return {
            'hours': decimal.Decimal(raw_data[0]['count'] *
                                     self.type_settings['period_length']
                                     ) / 60,
            'gb_size': raw_data[1]['metadata']['gb_size'],
            'type': 'volume:' + raw_data[1]['metadata']['type'],
            'res_string': 'volume:' + raw_data[1]['metadata']['type']
            + ':' + raw_data[1]['metadata']['display_name']}

    def _validate_params(self, params):
        super(VolumePriceCalculator, self)._validate_params(params)
        if decimal.Decimal(params['gb_size']) < decimal.Decimal(1.0):
            raise Exception('the given gb_size cannot be less than 1')


class InstancePriceCalculator(CalculatorBase):
    type_name = "instance"
    resource_type_relation = "resource__flavor__os_flavor_id"
    required_params = ['hours', 'flavor', 'res_string']
    optional_params = []
    type_key = "flavor"

    def _final_calculation(self, params):
        return (self._get_unit_price(params['flavor']) *
                decimal.Decimal(params['hours']))

    def _get_model(self):
        return models.Flavor

    def _get_params_from_raw_stats(self, raw_data):
        return {
            'hours': self.get_hours_from_periods(raw_data[0]['count']),
            'flavor': 'instance:' + raw_data[1]['metadata']['flavor.name'],
            'res_string': 'instance:' + raw_data[1]['metadata']['flavor.name']
            + ':' + raw_data[1]['metadata']['display_name']}
