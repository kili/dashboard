import datetime
from django.conf import settings
from django.db import utils
from keystoneclient.v2_0 import client
from user_billing import models


class StatisticsIndexBuilder(object):

    def __init__(self):
        self.ks_client = False
        self.uids = False
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
            brt = settings.BILLABLE_RESOURCE_TYPES
            self.meters = [y for x in brt.keys()
                           if 'meters' in brt[x]
                           for y in brt[x]['meters']]
        return self.meters

    def _list_ks_user_ids(self):
        if not self.uids:
            self.uids = [x.id for x in self._get_ks_client().users.list()]
        return self.uids

    def _merge_indexing_data(self):
        # define data collectors in dc
        dc = {'meters': self._list_billable_resource_type_meters,
              'uids': self._list_ks_user_ids,
              'month': self._get_last_month}

        # create a list of every possible combination of uid, meter and date
        return [dict({'user_id': uid, 'meter': meter}.items() +
                     dc['month']().items())
                for uid in dc['uids']()
                for meter in dc['meters']()]

    def _save_index(self, index_data):
        added_count = 0
        for index_element in index_data:
            try:
                models.RawStatisticsIndex.objects.create(**index_element)
                added_count += 1
            except utils.IntegrityError:
                pass
        return added_count

    def build(self):
        self._save_index(self._merge_indexing_data())
