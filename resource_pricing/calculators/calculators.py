import abc
import decimal
from django.conf import settings
from django.core import exceptions
from resource_pricing.models import Price


class CalculatorBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def meter_name():
        pass

    @abc.abstractproperty
    def resource_type_relation():
        pass

    @abc.abstractmethod
    def _final_price_calculation():
        """do the type specific calculations."""

    @classmethod
    def _get_unit_price(cls, type_id, currency="USD"):
        try:
            return Price.objects.get(
                **{"currency__iso": currency,
                   cls.resource_type_relation: type_id}).price
        except exceptions.ObjectDoesNotExist:
            raise Exception("Could not get price of id {0} in currency "
                            "{1}".format(type_id, currency))

    @classmethod
    def hours_from_periods(cls, periods):
        return (decimal.Decimal(
            settings.BILLABLE_RESOURCE_TYPES[cls.meter_name]['period_length'])
            * decimal.Decimal(periods) / decimal.Decimal(60))

    @classmethod
    def get_price_calculator(cls, meter):
        for price_calc_class in cls.__subclasses__():
            if price_calc_class.meter_name == meter:
                return price_calc_class()
        raise Exception(
            u'could not find price calculator class for {0}'.format(meter))

    @classmethod
    def price_from_stats(cls, stats):
        stats['price'] = cls._final_price_calculation(stats)
        return stats


class VolumePriceCalculator(CalculatorBase):
    meter_name = 'volume'
    resource_type_relation = 'resource__volumetype__os_volume_type_id'

    @classmethod
    def _final_price_calculation(cls, params):
        return (cls._get_unit_price(params['type']) *
                decimal.Decimal(params['gb_size']) *
                decimal.Decimal(params['hours']))


class InstancePriceCalculator(CalculatorBase):
    meter_name = 'instance'
    resource_type_relation = 'resource__instancetype__os_instance_type_id'

    @classmethod
    def _final_price_calculation(cls, params):
        return (cls._get_unit_price(params['flavor']) *
                decimal.Decimal(params['hours']))
