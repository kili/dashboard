from accounting.balance_limits import ThresholdAction
from notifications.notification_sender import Notifications


class SendNotificationThresholdAction(ThresholdAction):
    verbose_name = 'send_notification'

    @staticmethod
    def handler(**kwargs):
        Notifications.get_notification_sender('low_balance').add(**kwargs)
