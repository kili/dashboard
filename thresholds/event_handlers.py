from accounting.managers import AccountManager
from notifications.notification_sender import Notifications
from nova_wrapper.client import NovaClient
from thresholds.balance_thresholds import ThresholdActionBase


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
    def handler(cls, **kwargs):
        if AccountManager().get_user_account(
                kwargs['project_id']).balance() >= 0:
            return
        # need to enable all_tenants because of this (read comments):
        # https://bugs.launchpad.net/python-novaclient/+bug/1134382
        [server.stop() for server in NovaClient.get_client().servers.list(
            search_opts={'all_tenants': True,
                         'tenant_id': kwargs['project_id'],
                         'status': 'ACTIVE'})]
