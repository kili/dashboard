from optparse import make_option
from django.core.management.base import BaseCommand
from thresholds.balance_thresholds import ActionQueueProcessor


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--imsure',
                    action='store_true',
                    dest='imsure',
                    default=False),)

    def handle(self, *args, **kwargs):
        ActionQueueProcessor.process(dry_run=not kwargs['imsure'])
