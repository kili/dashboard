from django.conf import settings
from keystoneclient.v2_0 import client


class KeystoneClient(object):
    client = None

    @classmethod
    def get_client(cls):
        if not cls.client:
            cls.client = client.Client(
                token=settings.KEYSTONE_TOKEN,
                endpoint=settings.KEYSTONE_URL)
        return cls.client
