from accounting.transactions import UserTransactions
from resource_pricing.priced_usage import PricedUsageBase
from project_billing.helpers import FormattingHelpers
from project_billing.ceilometer_fetcher import StatsContainer
from project_billing.models import RawStatistics
from project_billing.models import RawStatisticsIndex


class AccountingTransactor(object):

    @classmethod
    def _get_raw_data(cls, id):
        return [StatsContainer.from_pickle_string(x.data) for x in
                RawStatistics.objects.filter(statistics_index=id)]

    @classmethod
    def _get_transaction_message(cls, resource):
        return u'{0} for {1} hours'.format(resource['res_string'],
                                           FormattingHelpers.hours(
                                               resource['hours']))

    @classmethod
    def _get_unbilled_statistics(cls):
        return RawStatisticsIndex.objects.filter(fetched=True,
                                                 has_data=True,
                                                 billed=False)

    @classmethod
    def _print_info(cls, project, priced_usage):
        print(u'dry run: proj {0}, price {1}, desc {2}'.format(
            project,
            FormattingHelpers.price(
                priced_usage['price']),
            cls._get_transaction_message(
                priced_usage)))

    @classmethod
    def bill_projects(cls, dry_run=False):
        ut = UserTransactions()
        for stat in cls._get_unbilled_statistics():
            for data in cls._get_raw_data(stat.id):
                for priced_usage in PricedUsageBase.get_meter_class(
                        stat.meter).get_priced_stats(data):
                    if not dry_run:
                        ut.consume_user_money(
                            stat.project_id,
                            priced_usage['price'],
                            cls._get_transaction_message(
                                priced_usage))
                        stat.billed = True
                        stat.save()
                    cls._print_info(stat.project_id, priced_usage)
