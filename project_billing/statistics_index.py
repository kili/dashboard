from django.conf import settings
from django.db import utils
from django.utils import timezone
from keystoneclient.v2_0 import client
from project_billing.models import RawStatistics
from project_billing.models import RawStatisticsIndex
from project_billing.ceilometer_fetcher import CeilometerStats


class StatisticsIndexBuilder(object):

    def __init__(self):
        self.ks_client = False
        self.project_ids = False
        self.meters = False
        self.timerange = False

    def _get_ks_client(self):
        if not self.ks_client:
            self.ks_client = client.Client(token=settings.KEYSTONE_TOKEN,
                                           endpoint=settings.KEYSTONE_URL)
        return self.ks_client

    def _get_time_range(self):
        if not self.timerange:
            self.timerange = {
                'from_ts': (timezone.now() -
                timezone.timedelta(days=1)).replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0),
                'until_ts': timezone.now().replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0)}
        return self.timerange

    def _list_billable_resource_type_meters(self):
        if not self.meters:
            self.meters = settings.BILLABLE_RESOURCE_TYPES.keys()
        return self.meters

    def _list_ks_project_ids(self):
        if not self.project_ids:
            self.project_ids = [
                x.id for x in self._get_ks_client().tenants.list()]
        return self.project_ids

    def _merge_indexing_data(self):
        # define data collectors in dc
        dc = {'meters': self._list_billable_resource_type_meters,
              'project_ids': self._list_ks_project_ids,
              'time_range': self._get_time_range()}

        # create every possible combination of projectid, meter and date
        return [dict({'project_id': project_id, 'meter': meter}.items() +
                     dc['time_range'].items())
                for project_id in dc['project_ids']()
                for meter in dc['meters']()]

    def _save_index(self, index_data):
        for index_element in index_data:
            try:
                RawStatisticsIndex.objects.create(**index_element)
            except utils.IntegrityError:
                # in case the previous run of this job has been aborted,
                # just continue where we stopped
                pass

    def build(self):
        self._save_index(self._merge_indexing_data())


class UnfetchedStatisticsFetcher(object):

    def _fetch_store_dataset(self, dataset):
        self._store(dataset, self._fetch(dataset))

    def _fetch(self, dataset):
        return CeilometerStats.get_stats(
            meter=dataset.meter,
            project_id=dataset.project_id,
            from_ts=dataset.from_ts,
            until_ts=dataset.until_ts)

    def _store(self, index, data):
        if data.has_data:
            self._store_with_data(
                index,
                data)
        index.fetched = True
        index.save()

    def _store_with_data(self, index, data):
        RawStatistics.objects.create(statistics_index=index,
                                            data=data.pickle())
        index.has_data = True

    def fetch(self):
        for unfetched_dataset in RawStatisticsIndex.objects.filter(
                fetched=False):
            self._fetch_store_dataset(unfetched_dataset)
