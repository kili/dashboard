from accounting import transactions
from resource_pricing import priced_usage
from user_billing import helpers
from user_billing.metering.ceilometer import data_fetcher
from user_billing import models


class UserTransactor(object):

    def __init__(self):
        self.ut = transactions.UserTransactions()

    def _get_raw_data(self, id):
        return [data_fetcher.StatsContainer.from_pickle_string(x.data) for x in
                models.RawStatistics.objects.filter(statistics_index=id)]

    def _get_transaction_message(self, resource, hours):
        return u'"{0}" for {1} hours'.format(resource,
                                             helpers.FormattingHelpers.hours(
                                                 hours))

    def _get_unbilled_statistics(self):
        return models.RawStatisticsIndex.objects.filter(fetched=True,
                                                        has_data=True,
                                                        billed=False)

    def bill_users(self, dry_run=False):
        for stat in self._get_unbilled_statistics():
            datasets = self._get_raw_data(stat.id)
            for data in datasets:
                priced_flavors = priced_usage.PricedUsageBase.get_meter_class(
                    stat.meter).get_priced_stats(data)
                for priced_flavor in priced_flavors:
                    if dry_run:
                        print(u'dry run: {0}, {1}, {2}'.format(
                            stat.project_id,
                            priced_flavor['price'],
                            self._get_transaction_message(
                                priced_flavor['res_string'],
                                priced_flavor['hours'])))
                        continue
                    self.ut.consume_user_money(
                        stat.project_id,
                        priced_flavor['price'],
                        self._get_transaction_message(
                            priced_flavor['res_string'],
                            priced_flavor['hours']))
                    stat.billed = True
                    stat.save()
