import datetime
from django.db import utils
import pickle
from user_billing.metering.ceilometer import data_fetcher
from user_billing import models


class UnfectedDataFetcher(object):

    has_more_data = 1

    def __init__(self):
        self.fetcher = data_fetcher.CeilometerDataFetcher()

    def _fetch_store_dataset(self, dataset):
        self._fetch(dataset)

    def _fetch(self, dataset):
        timerange = self._get_from_until_of_month({'month': dataset.month,
                                                   'year': dataset.year})
        self._store(dataset, self.fetcher.get(user_id=dataset.user_id,
                                              meter=dataset.meter,
                                              from_dt=timerange['from'],
                                              until_dt=timerange['until']))

    def _get_from_until_of_month(self, month):
        from_dt = datetime.datetime(month['year'], month['month'], 1)
        until_dt = (from_dt + datetime.timedelta(days=31)).replace(day=1)
        return {'from': from_dt, 'until': until_dt}

    def _get_unfetched_index(self):
        return models.RawStatisticsIndex.objects.filter(fetched=False)

    def _store(self, index, dataset):
        if len(dataset) > 0:
            self._store_with_data(index, dataset)
        else:
            index.fetched = True
            index.save()

    def _store_with_data(self, index, dataset):
        data_string = pickle.dumps(dataset[0].to_dict())
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
        index.fetched = True
        index.has_data = True
        index.save()

    def fetch(self, timespan=3600):
        for unfetched_dataset in self._get_unfetched_index():
            self._fetch_store_dataset(unfetched_dataset)
