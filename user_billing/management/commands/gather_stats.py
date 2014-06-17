from django.core.management import base
from user_billing import meter_index
from user_billing import transactor


class Command(base.BaseCommand):

    def handle(self, *args, **kwargs):
        meter_index.StatisticsIndexBuilder().build()
        meter_index.UnfectedDataFetcher().fetch()
        transactor.UserTransactor().bill_users()
