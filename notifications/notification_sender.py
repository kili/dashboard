import itertools
import logging
from django.conf import settings
from django.core.mail import send_mass_mail
from django.template import Context
from django.template.loader import get_template
from billing_app.utils import format_currency
from keystoneclient.apiclient.exceptions import NotFound
from keystone_wrapper.client import KeystoneClient


class NotificationSenderBase(object):
    params = ['project_id']
    currency_format_fields = []
    from_email = settings.DEFAULT_FROM_EMAIL

    def __init__(self):
        self.notifications = []

    def _lookup_email_address(self, project_id):
        return [x.email for x in
                KeystoneClient.get_client().tenants.get(
                    project_id).list_users()]

    def _format_currencies(self, notification, keys):
        for key in keys:
            notification[key] = format_currency(notification[key])
        return notification

    def add(self, **kwargs):
        notification = {x: kwargs[x] for x in self.params}
        try:
            notification['email'] = self._lookup_email_address(
                notification['project_id'])
            if len(notification['email']) == 0 or not notification['email'][0]:
                raise NotFound()
        except NotFound:
            logger = logging.getLogger('horizon')
            logger.warning('could not lookup email addresses for project {0}'
                           ', skipping'.format(notification['project_id']))
            return
        self.notifications.append(
            self._format_currencies(notification, self.currency_format_fields))

    def get_notifications(self):
        return [
            (self.subject,
             get_template(self.template).render(Context(notification)),
             self.from_email,
             notification['email'])
            for notification in self.notifications]


class LowBalanceNotificationSender(NotificationSenderBase):
    currency_format_fields = ['passed_limit', 'current_balance']
    name = 'low_balance'
    params = NotificationSenderBase.params + \
        ['passed_limit', 'current_balance']
    template = 'notifications/low_balance.txt'
    subject = 'Your balance is low'


class PromotionGrantedNotificationSender(NotificationSenderBase):
    currency_format_fields = ['promotion_amount', 'new_balance']
    name = 'promotion_granted'
    params = NotificationSenderBase.params + \
        ['promotion_amount', 'new_balance', 'message']
    template = 'notifications/promotion_granted.txt'
    subject = 'You received a promotion'


class Notifications(object):
    sender_instances = {}

    @classmethod
    def send_all_notifications(cls):
        send_mass_mail(cls.get_all_sender_notifications())
        cls.delete_all_notifications()

    @classmethod
    def delete_all_notifications(cls):
        cls.sender_instances = {}

    @classmethod
    def get_all_sender_notifications(cls):
        return list(itertools.chain(
            *[x.get_notifications() for x in cls.sender_instances.values()]))

    @classmethod
    def get_notification_sender(cls, sender_name):
        for subclass in NotificationSenderBase.__subclasses__():
            if subclass.name == sender_name:
                if (not sender_name in cls.sender_instances or
                    not isinstance(cls.sender_instances[sender_name],
                        subclass)):
                    cls.sender_instances[sender_name] = subclass()
                return cls.sender_instances[sender_name]
