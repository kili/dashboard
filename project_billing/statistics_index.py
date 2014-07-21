from django.conf import settings
from django.db import utils
from django.utils import timezone
from keystoneclient.v2_0 import client
from project_billing.helpers import FormattingHelpers
from project_billing.models import RawStatistics
from project_billing.models import RawStatisticsIndex
from project_billing.ceilometer_fetcher import CeilometerStats


class StatisticsIndexBuilder(object):

    def __init__(self):
        self.ks_client = False
        self.project_ids = False

    def _get_ks_client(self):
        if not self.ks_client:
            self.ks_client = client.Client(token=settings.KEYSTONE_TOKEN,
                                           endpoint=settings.KEYSTONE_URL)
        return self.ks_client

    def _get_time_range(self):
        if self.date:
            from_ts = FormattingHelpers.get_datetime(self.date)
        else:
            from_ts = timezone.now() - timezone.timedelta(days=1)
        return {
            'from_ts': from_ts.replace(hour=0,
                                       minute=0,
                                       second=0,
                                       microsecond=0),
            'until_ts': (from_ts +
                         timezone.timedelta(days=1)).replace(
                             hour=0,
                             minute=0,
                             second=0,
                             microsecond=0)}

    def _list_ks_project_ids(self):
        if not self.project_ids:
            self.project_ids = [
                x.id for x in self._get_ks_client().tenants.list()]
        return self.project_ids

    def _merge_indexing_data(self):
        # define data collectors in dc
        dc = {'meters': settings.BILLABLE_RESOURCE_TYPES.keys(),
              'project_ids': self._list_ks_project_ids(),
              'time_range': self._get_time_range()}

        # create every possible combination of projectid, meter and date
        return [dict({'project_id': project_id, 'meter': meter}.items() +
                     dc['time_range'].items())
                for project_id in dc['project_ids']
                for meter in dc['meters']]

    @staticmethod
    def _save_index(index_data):
        for index_element in index_data:
            try:
                RawStatisticsIndex.objects.create(**index_element)
            except utils.IntegrityError:
                # in case the previous run of this job has been aborted,
                # just continue where we stopped
                pass

    def build(self, date=None):
        self.date = date
        self._save_index(self._merge_indexing_data())


class UnfetchedStatisticsFetcher(object):

    @classmethod
    def _fetch_from_cm(cls, index):
        return CeilometerStats.get_stats(
            meter=index.meter,
            project_id=index.project_id,
            from_ts=index.from_ts,
            until_ts=index.until_ts)

    @classmethod
    def fetch(cls):
        for index in RawStatisticsIndex.objects.filter(fetched=False):
            data = cls._fetch_from_cm(index)
            if data.has_data:
                RawStatistics.objects.create(statistics_index=index,
                                             data=data.pickle())
                index.has_data = True
            index.fetched = True
            index.save()
