from resource_pricing.calculators.instance import calculator
from user_billing.metering.ceilometer import data_fetcher


class PricedUsageManager(object):

    @classmethod
    def get_overview(cls, project_id, timerange):
        return cls._get_priced_stats(cls._get_stats(project_id,
                                                    timerange))

    @classmethod
    def _get_priced_stats(cls, stats):
        retval = []
        ic = calculator.PriceCalculator()
        for flavor, stats in stats.get_merged_by(
                lambda x: x.metadata['flavor.name']).items():
            usage = ic.price_from_raw_stats('instance:' +
                                            flavor, stats['stats'].to_dict())
            usage['resource'] = flavor
            usage['id'] = stats['resource'].resource_id
            retval.append(usage)
        return retval

    @classmethod
    def _get_stats(cls, project_id, timerange):
        sq = data_fetcher.StatsQuery(project_id,
                                     'instance',
                                     timerange[0],
                                     timerange[1])
        return data_fetcher.CeilometerStats().get_stats(sq)
