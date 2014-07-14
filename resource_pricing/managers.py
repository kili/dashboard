from resource_pricing.calculators import calculators
from user_billing.metering.ceilometer import data_fetcher


class PricedUsageBase(object):

    @classmethod
    def get_overview(cls, project_id, timerange):
        return cls._get_priced_stats(cls.get_stats(project_id,
                                                   timerange))

    @classmethod
    def get_stats(cls, project_id, from_ts, until_ts):
        return data_fetcher.CeilometerStats().get_stats(
            data_fetcher.StatsQuery(project_id,
                                    cls.meter_name,
                                    from_ts,
                                    until_ts))


class PricedInstanceUsage(PricedUsageBase):

    meter_name = 'instance'

    @classmethod
    def _get_priced_stats(cls, stats):
        retval = []
        for name, stats in stats.get_merged_by(
                lambda x: x.metadata['display_name']).items():
            usage = calculators.InstancePriceCalculator().price_from_raw_stats(
                (stats['stats'].to_dict(),
                 stats['resource'].to_dict()))
            usage['name'] = name
            usage['flavor'] = stats['resource'].metadata['flavor.name']
            usage['id'] = stats['resource'].resource_id
            retval.append(usage)
        return retval
