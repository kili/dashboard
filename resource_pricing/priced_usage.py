import abc
from resource_pricing.calculators import calculators


class PricedUsageBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _merge_stats(cls, stats):
        """Method to merge stats in a way that makes sense for this
           resource type.
        """

    @abc.abstractmethod
    def get_priced_stats(cls, stats):
        """Method that fetches stats and combines them with prices."""

    @classmethod
    def get_meter_class(cls, meter):
        for meter_class in cls.__subclasses__():
            if meter_class.meter_name == meter:
                return meter_class
        raise Exception(u'could not find priced_usage class for {0}'.format(
            meter))


class PricedInstanceUsage(PricedUsageBase):

    meter_name = 'instance'

    @classmethod
    def _res_string_from_usage(cls, usage):
        return u'instances of flavor \'{0}\': {1}'.format(
            usage['flavor'],
            u', '.join([u'\'' + x + u'\'' for x in usage['resources']]))

    @classmethod
    def get_priced_stats(cls, stats):
        retval = []
        for name, stats in cls._merge_stats(stats).items():
            usage = calculators.CalculatorBase.get_price_calculator_of_meter(
                cls.meter_name).price_from_raw_stats(
                    [{'resource': x['resource'],
                      'stats': x['stats']} for x in stats])
            usage['res_string'] = cls._res_string_from_usage(usage)
            retval.append(usage)
        return retval

    @classmethod
    def _merge_stats(cls, stats):
        return stats.get_merged_by(lambda x: x['metadata']['flavor.id'])
