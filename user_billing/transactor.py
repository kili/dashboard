from accounting import transactions
from django.conf import settings
import importlib
import pickle
from user_billing import models


class UserTransactor(object):

    def __init__(self):
        self.ut = transactions.UserTransactions()

    def _get_price_calculator_of_meter(self, meter):
        brt = settings.BILLABLE_RESOURCE_TYPES
        pc_name = False
        for k, v in brt.items():
            if 'meters' not in v:
                continue
            if meter in v['meters']:
                pc_name = v['price_calculator']
                break
        return importlib.import_module(
            pc_name + '.calculator').PriceCalculator()

    def _get_raw_data(self, id):
        return pickle.loads(
            models.RawStatistics.objects.get(statistics_index=id).data)

    def _get_unbilled_statistics(self):
        return models.RawStatisticsIndex.objects.filter(fetched=True,
                                                        has_data=True,
                                                        billed=False)

    def bill_users(self):
        for stat in self._get_unbilled_statistics():
            data = self._get_raw_data(stat.id)
            try:
                pc = self._get_price_calculator_of_meter(stat.meter)
            except Exception:
                raise Exception('failed to get price calculator for {0}'
                                .format(stat.meter))
            self.ut.consume_user_money(
                stat.user_id,
                pc.price_from_raw_stats(stat.meter, data),
                stat.meter)
            stat.billed = True
            stat.save()

