import abc
from resource_pricing.calculators.calculators import CalculatorBase


class PricedUsageBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def meter_name(cls):
        pass

    @abc.abstractmethod
    def _extract_params_from_raw_stats(cls, raw_data):
        """extract the datapoints which are required to do price calculations
           from raw statistics.
        """

    @abc.abstractmethod
    def _merge_stats(cls, stats):
        """Method to merge stats in a way that makes sense for this
           resource type.
        """

    @abc.abstractmethod
    def get_priced_stats(cls, stats):
        """Method that fetches stats and combines them with prices."""

    @staticmethod
    def meter_specific_criterias(query):
        return query

    @classmethod
    def _price_calculator(cls):
        return CalculatorBase.get_price_calculator(cls.meter_name)

    @classmethod
    def get_meter_class(cls, meter):
        for meter_class in cls.__subclasses__():
            if meter_class.meter_name == meter:
                return meter_class
        raise Exception(
            u'could not find priced_usage class for {0}'.format(meter))


class PricedInstanceUsage(PricedUsageBase):
    meter_name = 'instance'

    @classmethod
    def _res_string_from_usage(cls, usage):
        return u'instances of flavor \'{0}\': {1}'.format(
            usage['flavor'],
            u', '.join([u'\'{0}\''.format(x) for x in usage['resources']]))

    @classmethod
    def _merge_stats(cls, stats):
        return stats.merged_by(lambda x: x['metadata']['flavor.id'])

    @classmethod
    def get_priced_stats(cls, stats):
        retval = []
        for stats in cls._merge_stats(stats).values():
            priced_usage = cls._price_calculator().price_from_stats(
                cls._extract_params_from_raw_stats(stats))
            priced_usage['res_string'] = cls._res_string_from_usage(
                priced_usage)
            retval.append(priced_usage)
        return retval

    @classmethod
    def _extract_params_from_raw_stats(cls, raw_data):
        if len(raw_data) < 1:
            raise Exception('received empty data')
        try:
            return {
                'id': raw_data[0]['resource']['metadata']['flavor.id'],
                'hours': cls._price_calculator().hours_from_periods(
                    sum([x['stats']['count'] for x in raw_data])),
                'flavor': u'instance:{0}'.format(
                    raw_data[0]['resource']['metadata']['flavor.name']),
                'resources': [x['resource']['metadata']['display_name']
                            for x in raw_data],
                'tenant_id': raw_data[0]['resource']['project_id']}
        except KeyError:
            raise Exception('received bad raw_statistics from ceilometer')

    @staticmethod
    def meter_specific_criterias(query):
        query['q'].append({'field': 'resource_metadata.status',
                           'op': 'eq',
                           'value': 'ACTIVE'})
        return query
