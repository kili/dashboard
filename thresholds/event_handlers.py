from django.conf import settings
from novaclient.v1_1 import client as novaclient
from accounting.managers import AccountManager
from thresholds.balance_thresholds import ThresholdActionBase
from notifications.notification_sender import Notifications


class SendNotificationThresholdAction(ThresholdActionBase):
    verbose_name = 'send_notification'

    @staticmethod
    def handler(**kwargs):
        Notifications.get_notification_sender('low_balance').add(**kwargs)


class StopProjectInstancesThresholdAction(ThresholdActionBase):
    _novaclient = None
    delay = 345600  # 4 days
    verbose_name = 'stop_project_instances'

    @classmethod
    def _get_novaclient(cls):
        if not cls._novaclient:
            cls._novaclient = novaclient.Client(
                settings.ADMIN_AUTH_DATA['os_username'],
                settings.ADMIN_AUTH_DATA['os_password'],
                settings.ADMIN_AUTH_DATA['os_tenant_name'],
                auth_url=settings.ADMIN_AUTH_DATA['os_auth_url'])
        return cls._novaclient

    @classmethod
    def handler(cls, **kwargs):
        if AccountManager().get_user_account(
                kwargs['project_id']).balance() >= 0:
            return
        # need to enable all_tenants because of this (read comments):
        # https://bugs.launchpad.net/python-novaclient/+bug/1134382
        [server.stop() for server in cls._get_novaclient().servers.list(
            search_opts={'all_tenants': True,
                         'tenant_id': kwargs['project_id'],
                         'status': 'ACTIVE'})]
