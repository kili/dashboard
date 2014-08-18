from accounting.transactions import UserTransactions
from keystone_wrapper.client import KeystoneClient
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
    def _resolve_project_name(cls, id):
        try:
            return KeystoneClient.get_client().tenants.get(
                tenant_id=id).name
        except Exception:
            return ''

    @classmethod
    def _print_info(cls, project, priced_usage, dry_run=False):
        msg = u'proj {0}({1}), price {2}, desc {3}'.format(
            cls._resolve_project_name(project),
            project,
            FormattingHelpers.price(
                priced_usage['price']),
            cls._get_transaction_message(
                priced_usage))
        if dry_run:
            msg = u'dry run: {0}'.format(msg)
        print(msg)

    @classmethod
    def bill_projects(cls, dry_run=False):
        ut = UserTransactions()
        for stat in cls._get_unbilled_statistics():
            for data in cls._get_raw_data(stat.id):
                for priced_usage in PricedUsageBase.get_meter_class(
                        stat.meter).get_priced_stats(
                            data,
                            (stat.from_ts,
                             stat.until_ts)):
                    if not dry_run:
                        ut.consume_user_money(
                            stat.project_id,
                            priced_usage['price'],
                            cls._get_transaction_message(
                                priced_usage))
                        stat.billed = True
                        stat.save()
                    cls._print_info(stat.project_id, priced_usage, dry_run)
