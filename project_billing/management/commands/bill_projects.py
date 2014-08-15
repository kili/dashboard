from optparse import make_option
from django.core.management.base import BaseCommand
from notifications.notification_sender import Notifications
from project_billing.helpers import FormattingHelpers
from project_billing.statistics_index import StatisticsIndexBuilder
from project_billing.statistics_index import UnfetchedStatisticsFetcher
from project_billing.transactor import AccountingTransactor


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--imsure',
                    action='store_true',
                    dest='imsure',
                    default=False),
        make_option('--date',
                    action='callback',
                    dest='date',
                    type='string',
                    callback=FormattingHelpers.verify_input_date))

    def handle(self, *args, **kwargs):
        StatisticsIndexBuilder().build(date=kwargs['date'])
        UnfetchedStatisticsFetcher.fetch()
        AccountingTransactor.bill_projects(dry_run=(not kwargs['imsure']))
        Notifications.send_all_notifcations()
