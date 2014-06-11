import datetime
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
        self._store(self.fetcher.get(user_id=dataset.user_id,
                                     meter=dataset.meter,
                                     from_dt=timerange['from'],
                                     until_dt=timerange['until']))

    def _get_from_until_of_month(self, month):
        from_dt = datetime.datetime(month['year'], month['month'], 1)
        until_dt = (from_dt + datetime.timedelta(days=31)).replace(day=1)
        return {'from': from_dt, 'until': until_dt}

    def _get_unfetched_index(self):
        return models.RawStatisticsIndex.objects.filter(fetched=False)

    def _store(self, dataset):
        pass

    def fetch(self, timespan=3600):
        for unfetched_dataset in self._get_unfetched_index():
            self._fetch_store_dataset(unfetched_dataset)
