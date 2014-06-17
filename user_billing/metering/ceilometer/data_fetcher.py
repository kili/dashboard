from ceilometerclient import client
from django.conf import settings
from keystoneclient import exceptions as ks_exceptions


class CeilometerDataFetcher(object):

    def __init__(self):
        try:
            self.cm_client = client.get_client(
                settings.CEILOMETER_API_VERSION,
                **settings.CEILOMETER_AUTH_DATA)
        except ks_exceptions.AuthorizationFailure:
            raise Exception("failed to connect/authenticate to ceilometer")

    def _datetime_to_mongo(self, datetime):
        return datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def _get_query(self, *args, **kwargs):
        return {'meter_name': kwargs['meter'],
                'q': [{'field': 'project_id', 'op': 'eq',
                       'value': kwargs['project_id']},
                      {'field': 'timestamp', 'op': 'ge',
                       'value': self._datetime_to_mongo(kwargs['from_dt'])},
                      {'field': 'timestamp', 'op': 'lt',
                       'value': self._datetime_to_mongo(kwargs['until_dt'])}]}

    def get(self, **kwargs):
        return self.cm_client.statistics.list(**self._get_query(**kwargs))


class QueryTimeRange(object):

    def __init__(self, from_dt, until_dt):
        self.from_dt = self._convert_to_mongo(from_dt)
        self.until_dt = self._convert_to_mongo(until_dt)

    def _convert_to_mongo(self, dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%S")

    def get_from(self):
        return self.from_dt

    def get_until(self):
        return self.until_dt


class StatsQuery(object):

    def __init__(self, project, meter, from_dt, until_dt):
        self.meter = meter
        self.timerange = QueryTimeRange(from_dt, until_dt)
        self.project = project

    def get_stats_query(self):
        return {'q': [{'field': 'project_id',
                       'op': 'eq',
                       'value': self.get_project()},
                      {'field': 'timestamp',
                       'op': 'ge',
                       'value': self.get_timerange().get_from()},
                      {'field': 'timestamp',
                       'op': 'lt',
                       'value': self.get_timerange().get_until()}],
                'groupby': ['resource_id']}

    def get_meter(self):
        return self.meter

    def get_timerange(self):
        return self.timerange

    def get_project(self):
        return self.project


class StatsContainer(object):

    def __init__(self, stats, resources):
        self.stats = stats
        self.resources = resources

    def _get_resource(self, res_id):
        for resource in self.resources:
            if resource.resource_id == res_id:
                return resource

    def count_datasets(self):
        return len(self.stats)

    def get_merged_by(self, keygen):
        retval = {}
        for stat in self.stats:
            res = self._get_resource(stat.groupby['resource_id'])
            retval[keygen(res)] = {'stats': stat, 'resource': res}
        return retval

    def get_stats(self):
        return self.stats


class CeilometerStats(object):

    def __init__(self):
        try:
            self.cm_client = client.get_client(
                settings.CEILOMETER_API_VERSION,
                **settings.CEILOMETER_AUTH_DATA)
        except ks_exceptions.AuthorizationFailure:
            raise Exception("failed to connect/authenticate to ceilometer")

    def _extract_resource_ids(self, stats):
        return [stat.groupby['resource_id'] for stat in stats]

    def _get_stats(self, cm_query):
        return self.cm_client.statistics.list(cm_query.get_meter(),
                                              **cm_query.get_stats_query())

    def _get_resources(self, res_ids):
        return map(self.cm_client.resources.get, res_ids)

    def get_stats(self, cm_query):
        stats = self._get_stats(cm_query)
        return StatsContainer(
            stats, self._get_resources(self._extract_resource_ids(stats)))
