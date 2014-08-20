from thresholds.balance_thresholds import ThresholdActionBase
from notifications.notification_sender import Notifications


class SendNotificationThresholdAction(ThresholdActionBase):
    verbose_name = 'send_notification'

    @staticmethod
    def handler(**kwargs):
        Notifications.get_notification_sender('low_balance').add(**kwargs)
