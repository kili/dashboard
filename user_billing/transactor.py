from accounting import transactions
from django.conf import settings
import importlib
import pickle
from user_billing import helpers
from user_billing import models


class UserTransactor(object):

    def __init__(self):
        self.ut = transactions.UserTransactions()

    def _get_price_calculator_of_meter(self, meter):
        brt = settings.BILLABLE_RESOURCE_TYPES
        pc_name = ""
        for k, v in brt.items():
            if (k == meter):
                pc_name = v['price_calculator']
                break
        return importlib.import_module(
            pc_name + '.calculator').PriceCalculator()

    def _get_raw_data(self, id):
        return [pickle.loads(x.data) for x in
                models.RawStatistics.objects.filter(statistics_index=id)]

    def _get_transaction_message(self, resource, hours):
        return u'{0} usage: {1} hours'.format(resource,
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
                try:
                    pc = self._get_price_calculator_of_meter(stat.meter)
                except Exception:
                    raise Exception('failed to get price calculator for {0}'
                                    .format(stat.meter))
                price_result = pc.price_from_raw_stats(stat.meter, data)
                if dry_run:
                    print('{0}, {1}, {2}'.format(
                        stat.project_id,
                        price_result['price'],
                        self._get_transaction_message(
                            price_result['res_string'],
                            price_result['hours'])))
                    continue
                self.ut.consume_user_money(
                    stat.project_id,
                    price_result['price'],
                    self._get_transaction_message(
                        price_result['res_string'],
                        price_result['hours']))
                stat.billed = True
                stat.save()
