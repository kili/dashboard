from django.conf import settings
from horizon.utils import memoized
from novaclient.v1_1 import client as novaclient


class NovaClient(object):
    _client = None

    @classmethod
    def get_client(cls):
        if not cls._client:
            cls._client = novaclient.Client(
                settings.ADMIN_AUTH_DATA['os_username'],
                settings.ADMIN_AUTH_DATA['os_password'],
                settings.ADMIN_AUTH_DATA['os_tenant_name'],
                auth_url=settings.ADMIN_AUTH_DATA['os_auth_url'])
        return cls._client

    @staticmethod
    @memoized.memoized_method
    def instance_type_id_to_name(id):
        return NovaClient.get_client().flavors.get(id).name

    @staticmethod
    @memoized.memoized_method
    def instance_type_name_to_id(name):
        return NovaClient.get_client().flavors.find(name=name).id
