from django.core.management import base
from user_billing import statistics_index
from user_billing import transactor


class Command(base.BaseCommand):

    def handle(self, *args, **kwargs):
        statistics_index.StatisticsIndexBuilder().build()
        statistics_index.UnfetchedStatisticsFetcher().fetch()
        if 'imsure' in args:
            transactor.UserTransactor().bill_users()
        else:
            transactor.UserTransactor().bill_users(dry_run=True)
