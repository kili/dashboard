from itertools import groupby
import pickle
from ceilometerclient import client
from django.conf import settings
from keystoneclient import exceptions as ks_exceptions


# must be singleton to prevent unnecessary reconnects to ceilometer-api
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


class StatsContainer(object):

    def __init__(self, stats, resources):
        self.stats = stats
        self.resources = resources

    def _get_resource(self, res_id):
        for resource in self.resources:
            if resource['resource_id'] == res_id:
                return resource
        raise Exception('corrupt data in StatsContainer')

    @classmethod
    def from_pickle_string(cls, string):
        unpickled = pickle.loads(string)
        return cls(unpickled['stats'], unpickled['resources'])

    @property
    def has_data(self):
        if len(self.stats) > 0:
            return True
        return False

    # merge stats and resource by a key that's produced by the given keygen
    def merged_by(self, keygen):
        def key_from_stat(data):
            return keygen(data['resource'])
        return {k: list(v) for k, v in
                groupby(
                    sorted(
                        [{'stats': x,
                          'resource': self._get_resource(
                              x['groupby']['resource_id'])}
                         for x in self.stats],
                        key=key_from_stat),
                    key=key_from_stat)}

    def pickle(self):
        return pickle.dumps({'stats': self.stats, 'resources': self.resources})


class CeilometerStats(object):

    @classmethod
    def _datetime_to_mongo(cls, ts):
        return ts.strftime('%Y-%m-%dT%H:%M:%S')

    @classmethod
    def _get_stats_query(cls, **kwargs):
        return {'q': [{'field': 'project_id',
                       'op': 'eq',
                       'value': kwargs['project_id']},
                      {'field': 'timestamp',
                       'op': 'ge',
                       'value': cls._datetime_to_mongo(kwargs['from_ts'])},
                      {'field': 'timestamp',
                       'op': 'lt',
                       'value': cls._datetime_to_mongo(kwargs['until_ts'])}],
                'groupby': ['resource_id']}

    @classmethod
    def get_stats(cls, **kwargs):
        stats = CeilometerClient().statistics.list(
            kwargs['meter'], **cls._get_stats_query(**kwargs))
        return StatsContainer(
            [x.to_dict() for x in stats],
            [x.to_dict() for x in map(CeilometerClient().resources.get,
                [stat.groupby['resource_id'] for stat in stats])])
