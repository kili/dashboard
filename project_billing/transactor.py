from accounting.transactions import UserTransactions
from resource_pricing.priced_usage import PricedUsageBase
from project_billing.helpers import FormattingHelpers
from project_billing.ceilometer_fetcher import StatsContainer
from project_billing.models import RawStatistics
from project_billing.models import RawStatisticsIndex


class UserTransactor(object):

    def __init__(self):
        self.ut = UserTransactions()

    def _get_raw_data(self, id):
        return [StatsContainer.from_pickle_string(x.data) for x in
                RawStatistics.objects.filter(statistics_index=id)]

    def _get_transaction_message(self, resource):
        return u'{0} for {1} hours'.format(resource['res_string'],
                                           FormattingHelpers.hours(
                                               resource['hours']))

    def _get_unbilled_statistics(self):
        return RawStatisticsIndex.objects.filter(fetched=True,
                                                        has_data=True,
                                                        billed=False)

    def bill_users(self, dry_run=False):
        for stat in self._get_unbilled_statistics():
            for data in self._get_raw_data(stat.id):
                for priced_flavor_usage in PricedUsageBase.get_meter_class(
                        stat.meter).get_priced_stats(data):
                    if dry_run:
                        print(u'dry run: proj {0}, price {1}, desc {2}'.format(
                            stat.project_id,
                            FormattingHelpers.price(
                                priced_flavor_usage['price']),
                            self._get_transaction_message(
                                priced_flavor_usage)))
                        continue
                    self.ut.consume_user_money(
                        stat.project_id,
                        priced_flavor_usage['price'],
                        self._get_transaction_message(
                            priced_flavor_usage['res_string'],
                            priced_flavor_usage['hours']))
                    stat.billed = True
                    stat.save()
