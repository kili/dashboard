from resource_pricing.calculators.instance import calculator \
    as instance_calculator
from user_billing.metering.ceilometer import data_fetcher


class PricedUsageBase(object):

    @classmethod
    def get_overview(cls, project_id, timerange):
        return cls._get_priced_stats(cls._get_stats(project_id,
                                                    timerange))

    @classmethod
    def _get_stats(cls, project_id, timerange):
        sq = data_fetcher.StatsQuery(project_id,
                                     cls.meter_name,
                                     timerange[0],
                                     timerange[1])
        return data_fetcher.CeilometerStats().get_stats(sq)


class PricedInstanceUsage(PricedUsageBase):

    meter_name = 'instance'

    @classmethod
    def _get_priced_stats(cls, stats):
        retval = []
        for name, stats in stats.get_merged_by(
                lambda x: x.metadata['display_name']).items():
            flavor = stats['resource'].metadata['flavor.name']
            ic = instance_calculator.PriceCalculator()
            usage = ic.price_from_raw_stats((stats['stats'].to_dict(),
                                             stats['resource'].to_dict()))
            usage['name'] = name
            usage['flavor'] = flavor
            usage['id'] = stats['resource'].resource_id
            retval.append(usage)
        return retval
