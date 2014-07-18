import pickle
from ceilometerclient import client
from django.conf import settings
from keystoneclient import exceptions as ks_exceptions


class CeilometerClient(object):
    _cm_client = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not cls._cm_client:
            cls._cm_client = object.__new__(cls)
            try:
                cls._cm_client = client.get_client(
                    settings.CEILOMETER_API_VERSION,
                    **settings.CEILOMETER_AUTH_DATA)
            except ks_exceptions.AuthorizationFailure:
                raise Exception('failed to connect/authenticate to ceilometer')
        return cls._cm_client


class QueryTimeRange(object):

    def __init__(self, from_ts, until_ts):
        self._from_ts = self._convert_to_mongo(from_ts)
        self._until_ts = self._convert_to_mongo(until_ts)

    def _convert_to_mongo(self, ts):
        return ts.strftime('%Y-%m-%dT%H:%M:%S')

    @property
    def from_ts(self):
        return self._from_ts

    @property
    def until_ts(self):
        return self._until_ts


class StatsQuery(object):

    def __init__(self, **kwargs):
        self.meter = kwargs['meter']
        self.project_id = kwargs['project_id']
        self.timerange = QueryTimeRange(kwargs['from_ts'],
                                        kwargs['until_ts'])

    def get_stats_query(self):
        return {'q': [{'field': 'project_id',
                       'op': 'eq',
                       'value': self.project_id},
                      {'field': 'timestamp',
                       'op': 'ge',
                       'value': self.timerange.from_ts},
                      {'field': 'timestamp',
                       'op': 'lt',
                       'value': self.timerange.until_ts}],
                'groupby': ['resource_id']}


class StatsContainer(object):

    def __init__(self, stats, resources):
        self.stats = stats
        self.resources = resources

    def _get_resource(self, res_id):
        for resource in self.resources:
            if resource['resource_id'] == res_id:
                return resource

    @property
    def has_data(self):
        if len(self.stats) > 0:
            return True
        return False

    def pickle(self):
        return pickle.dumps({
            'stats': self.stats,
            'resources': self.resources})

    @classmethod
    def from_pickle_string(cls, string):
        unpickled = pickle.loads(string)
        return cls(unpickled['stats'], unpickled['resources'])

    def count_datasets(self):
        return len(self.stats)

    def get_merged_by(self, keygen):
        retval = {}
        for stat in self.stats:
            res = self._get_resource(stat['groupby']['resource_id'])
            if keygen(res) not in retval:
                retval[keygen(res)] = []
            retval[keygen(res)].append({'stats': stat, 'resource': res})
        return retval

    def get_stats(self):
        return self.stats


class CeilometerStats(object):

    def _extract_resource_ids(self, stats):
        return [stat.groupby['resource_id'] for stat in stats]

    def _get_stats(self, cm_query):
        return CeilometerClient().statistics.list(cm_query.meter,
                                                  **cm_query.get_stats_query())

    def _get_resources(self, res_ids):
        return map(CeilometerClient().resources.get, res_ids)

    def get_stats(self, cm_query):
        stats = self._get_stats(cm_query)
        return StatsContainer(
            [x.to_dict() for x in stats],
            [x.to_dict() for x in self._get_resources(
                self._extract_resource_ids(stats))])
