from accounting import transactions
import pickle
from resource_pricing.calculators import calculators
from user_billing import helpers
from user_billing import models


class UserTransactor(object):

    def __init__(self):
        self.ut = transactions.UserTransactions()

    def _get_raw_data(self, id):
        return [pickle.loads(x.data) for x in
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
                pc = calculators.CalculatorBase.get_price_calculator_of_meter(
                    stat.meter)
                price_result = pc.price_from_raw_stats(data)
                if dry_run:
                    print(u'{0}, {1}, {2}'.format(
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
