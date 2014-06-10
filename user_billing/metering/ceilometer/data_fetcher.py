from ceilometerclient import client
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.core import exceptions as django_exceptions
from django.utils import timezone
from keystoneclient import exceptions as ks_exceptions
from user_billing.metering.ceilometer import models


class CeilometerDataFetcher(object):

    def __init__(self, meter_name, iter_time_span=3600):
        try:
            self.cm_client = client.get_client(
                settings.CEILOMETER_API_VERSION,
                **settings.CEILOMETER_AUTH_DATA)
        except ks_exceptions.AuthorizationFailure:
            raise Exception("failed to authenticate to ceilometer")
        self.iter_time_span = iter_time_span
        self.meter_name = meter_name
        try:
            self.position = models.CeilometerFetcherPosition.objects.get(
                meter_name=self.meter_name)
        except django_exceptions.ObjectDoesNotExist:
            self.position = models.CeilometerFetcherPosition.objects.create(
                meter_name=self.meter_name,
                position=datetime.datetime.utcnow())
        self.position_dt = self.position.position
        self._set_until_dt()
        self.finished = False

    def __iter__(self):
        return self

    def _set_until_dt(self):
        until_dt = self.position.position + timedelta(
            seconds=self.iter_time_span)
        if until_dt > timezone.now():
            until_dt = timezone.now()
            self.finished = True
        self.until_dt = until_dt

    def _get_query(self):
        return {'meter_name': self.meter_name,
                'q': [{'field': 'timestamp',
                       'op': 'gt', 'value': self._datetime_to_mongo(
                       self.position_dt)},
                      {'field': 'timestamp',
                       'op': 'le', 'value': self._datetime_to_mongo(
                       self.until_dt)}]}

    def _datetime_to_mongo(self, datetime):
        return datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def confirm_data_is_received(self):
        self.position.position = self.until_dt
        self.position.save()
        self.position_dt = self.until_dt
        self._set_until_dt()

    def next(self):
        if self.finished:
            raise StopIteration
        return self.cm_client.statistics.list(**self._get_query())
