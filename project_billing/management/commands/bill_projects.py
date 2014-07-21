from optparse import make_option
from django.core.management.base import BaseCommand
from project_billing.statistics_index import StatisticsIndexBuilder
from project_billing.statistics_index import UnfetchedStatisticsFetcher
from project_billing.transactor import AccountingTransactor


class Command(BaseCommand):
    args = 'imsure'
    option_list = BaseCommand.option_list + (
        make_option('--imsure',
                    action='store_true',
                    dest='imsure',
                    default=False),)

    def handle(self, *args, **kwargs):
        StatisticsIndexBuilder().build()
        UnfetchedStatisticsFetcher.fetch()
        AccountingTransactor.bill_projects(dry_run=(not kwargs['imsure']))
