import abc
import decimal
from django.conf import settings
from django.core import exceptions
from resource_pricing import models as pricing_models


class CalculatorBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def meter_name(self):
        pass

    @abc.abstractproperty
    def resource_type_relation(self):
        pass

    @abc.abstractmethod
    def _final_price_calculation(self, params):
        """do the type specific calculations."""

    def __init__(self):
        if self.meter_name not in settings.BILLABLE_RESOURCE_TYPES.keys():
            raise Exception("the type {0} is not configured".format(
                self.meter_name))
        self.type_settings = settings.BILLABLE_RESOURCE_TYPES[self.meter_name]

    def _get_unit_price(self, type_id, currency="USD"):
        try:
            return pricing_models.Price.objects.get(
                **{"currency__iso": currency,
                   self.resource_type_relation: type_id}).price
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not get price of id {0} in currency "
                            "{1}".format(type_id, currency))

    def hours_from_periods(self, periods):
        return (decimal.Decimal(self.type_settings['period_length'])
                * decimal.Decimal(periods) / decimal.Decimal(60))

    @classmethod
    def get_price_calculator(cls, meter):
        for price_calc_class in cls.__subclasses__():
            if price_calc_class.meter_name == meter:
                return price_calc_class()
        raise Exception(
            u'could not find price calculator class for {0}'.format(meter))

    def price_from_stats(self, stats):
        stats['price'] = self._final_price_calculation(stats)
        return stats


class VolumePriceCalculator(CalculatorBase):
    meter_name = 'volume'
    resource_type_relation = 'resource__volumetype__os_volume_type_id'

    def _final_price_calculation(self, params):
        return (self._get_unit_price(params['type']) *
                decimal.Decimal(params['gb_size']) *
                decimal.Decimal(params['hours']))


class InstancePriceCalculator(CalculatorBase):
    meter_name = 'instance'
    resource_type_relation = 'resource__instancetype__os_instance_type_id'

    def _final_price_calculation(self, params):
        return (self._get_unit_price(params['flavor']) *
                decimal.Decimal(params['hours']))
