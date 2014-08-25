from django.core.management.base import BaseCommand
from thresholds.balance_thresholds import ActionQueueProcessor


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        ActionQueueProcessor.process()
