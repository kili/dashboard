from datetime import datetime
from django.conf import settings
from user_billing.metering.ceilometer import data_fetcher
from resource_pricing.calculators.instance import calculator


class PricedUsageManager(object):

    @classmethod
    def get_overview(cls, user):
        return cls._get_priced_stats(cls._get_stats(user))

    @classmethod
    def _get_priced_stats(cls, stats):
        retval = []
        ic = calculator.PriceCalculator()
        for flavor, stats in stats.get_merged_by(
                lambda x: x.metadata['flavor.name']).items():
            usage = ic.price_from_raw_stats('instance:' + flavor, stats['stats'].to_dict())
            usage['resource'] = flavor
            usage['id'] = stats['resource'].resource_id
            retval.append(usage)
        return retval

    @classmethod
    def _get_stats(cls, user):
        sq = data_fetcher.StatsQuery(user,
                                     'instance',
                                     datetime(2014,1,1),
                                     datetime(2014,7,1))
        return data_fetcher.CeilometerStats().get_stats(sq)
