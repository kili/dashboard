from django.core.management import base
from user_billing import raw_data_fetcher
from user_billing import statistics_index_builder


class Command(base.BaseCommand):

    def handle(self, *args, **kwargs):
        statistics_index_builder.StatisticsIndexBuilder().build()
        raw_data_fetcher.RawDataFetcher().fetch()
