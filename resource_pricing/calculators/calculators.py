import abc
import decimal
from django.conf import settings
from django.core import exceptions
import importlib
from resource_pricing.calculators import models
from resource_pricing import models as pricing_models


class CalculatorBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        if self.type_name not in settings.BILLABLE_RESOURCE_TYPES.keys():
            raise Exception("the type {0} is not configured".format(
                self.type_name))
        self.type_settings = settings.BILLABLE_RESOURCE_TYPES[self.type_name]

    @abc.abstractmethod
    def _final_price_calculation(self, params):
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
                            "{1}".format(type_id, currency))

    def hours_from_periods(self, periods):
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
        params['price'] = self._final_price_calculation(params)
        return params


class VolumePriceCalculator(CalculatorBase):
    type_name = 'volume'
    resource_type_relation = 'resource__volumetype__os_volume_type_id'
    type_key = 'type'

    def _final_price_calculation(self, params):
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
            'type': u'volume:{0}'.format(raw_data[1]['metadata']['type']),
            'res_string': u'volume:{0}:{1}'.format(
                raw_data[1]['metadata']['type'],
                raw_data[1]['metadata']['display_name'])}


class InstancePriceCalculator(CalculatorBase):
    type_name = 'instance'
    resource_type_relation = 'resource__instancetype__os_instance_type_id'
    type_key = 'flavor'

    def _final_price_calculation(self, params):
        return (self._get_unit_price(params['flavor']) *
                decimal.Decimal(params['hours']))

    def _get_model(self):
        return models.Flavor

    def _get_params_from_raw_stats(self, raw_data):
        if len(raw_data) < 1:
            raise Exception('received bad data')
        period_count = 0
        for instance in raw_data:
            period_count += instance['stats']['count']
        return {
            'hours': self.hours_from_periods(period_count),
            'id': raw_data[0]['resource']['metadata']['flavor.id'],
            'flavor': u'instance:{0}'.format(
                raw_data[0]['resource']['metadata']['flavor.name']),
            'resources': [x['resource']['metadata']['display_name']
                    for x in raw_data]}
