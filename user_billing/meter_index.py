import datetime
from django.conf import settings
from django.db import utils
from keystoneclient.v2_0 import client
import pickle
from resource_pricing import managers
from user_billing import models


class StatisticsIndexBuilder(object):

    def __init__(self):
        self.ks_client = False
        self.project_ids = False
        self.meters = False
        self.month = False

    def _get_ks_client(self):
        if not self.ks_client:
            self.ks_client = client.Client(token=settings.KEYSTONE_TOKEN,
                                           endpoint=settings.KEYSTONE_URL)
        return self.ks_client

    def _get_last_month(self):
        if not self.month:
            last_month = (datetime.datetime.utcnow().replace(day=1)
                          - datetime.timedelta(days=1))
            self.month = {'year': last_month.year,
                          'month': last_month.month + 1}
        return self.month

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
              'month': self._get_last_month}

        # create every possible combination of projectid, meter and date
        return [dict({'project_id': project_id, 'meter': meter}.items() +
                     dc['month']().items())
                for project_id in dc['project_ids']()
                for meter in dc['meters']()]

    def _save_index(self, index_data):
        for index_element in index_data:
            try:
                models.RawStatisticsIndex.objects.create(**index_element)
            except utils.IntegrityError:
                pass

    def build(self):
        self._save_index(self._merge_indexing_data())


class UnfectedDataFetcher(object):

    def _fetch_store_dataset(self, dataset):
        self._store(dataset, self._fetch(dataset))

    def _fetch(self, dataset):
        return managers.PricedInstanceUsage.get_stats(
            dataset.project_id,
            self._get_from_until_of_month(
                {'month': dataset.month,
                 'year': dataset.year})).get_merged_by(
                     lambda x: x.metadata['display_name'])

    def _get_from_until_of_month(self, month):
        from_dt = datetime.datetime(month['year'], month['month'], 1)
        until_dt = (from_dt + datetime.timedelta(days=31)).replace(day=1)
        return (from_dt, until_dt)

    def _get_unfetched_index(self):
        return models.RawStatisticsIndex.objects.filter(fetched=False)

    def _store(self, index, datasets):
        for dataset in datasets.values():
            self._store_with_data(index, (dataset['stats'].to_dict(),
                                          dataset['resource'].to_dict()))
        index.fetched = True
        index.save()

    def _store_with_data(self, index, dataset):
        data_string = pickle.dumps(dataset)
        try:
            models.RawStatistics.objects.create(statistics_index=index,
                                                data=data_string)
        except utils.IntegrityError:
            # in case the previous run has been aborted between inserting the
            # data and updating the index just update the datatable with the
            # current data
            statistic = models.RawStatistics.objects.get(
                statistics_index=index)
            statistic.data = data_string
            statistic.save()
        index.has_data = True

    def fetch(self, timespan=3600):
        for unfetched_dataset in self._get_unfetched_index():
            self._fetch_store_dataset(unfetched_dataset)
