from django.core.management import base
from project_billing.statistics_index import StatisticsIndexBuilder
from project_billing.statistics_index import UnfetchedStatisticsFetcher
from project_billing.transactor import AccountingTransactor


class Command(base.BaseCommand):

    def handle(self, *args, **kwargs):
        StatisticsIndexBuilder().build()
        UnfetchedStatisticsFetcher.fetch()
        if 'imsure' in args:
            AccountingTransactor.bill_projects()
        else:
            AccountingTransactor.bill_projects(dry_run=True)
