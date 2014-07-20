from django.core.management import base
from project_billing.statistics_index import StatisticsIndexBuilder
from project_billing.statistics_index import UnfetchedStatisticsFetcher
from project_billing.transactor import UserTransactor


class Command(base.BaseCommand):

    def handle(self, *args, **kwargs):
        StatisticsIndexBuilder().build()
        UnfetchedStatisticsFetcher().fetch()
        if 'imsure' in args:
            UserTransactor().bill_users()
        else:
            UserTransactor().bill_users(dry_run=True)
