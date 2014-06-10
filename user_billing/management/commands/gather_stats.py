from django.core.management import base
from user_billing import statistics_index_builder
from user_billing import unfetched_data_fetcher


class Command(base.BaseCommand):

    def handle(self, *args, **kwargs):
        statistics_index_builder.StatisticsIndexBuilder().build()
        unfetched_data_fetcher.UnfectedDataFetcher().fetch()
