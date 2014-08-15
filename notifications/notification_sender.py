import itertools
from django.core.mail import send_mass_mail
from django.template import Context
from django.template.loader import get_template
from keystone_wrapper.client import KeystoneClientSingleton


class Notifications(object):
    sender_instances = {}
    params = ['project_id']
    notifications = []
    from_email = 'help@kili.io'

    @classmethod
    def send_all_notifications(cls):
        send_mass_mail(cls.get_all_sender_notifications())

    @classmethod
    def get_all_sender_notifications(cls):
        return list(itertools.chain(
            *[x.get_notifications() for x in cls.sender_instances.values()]))

    @classmethod
    def get_notification_sender(cls, sender_name):
        for subclass in cls.__subclasses__():
            if subclass.name == sender_name:
                if (not sender_name in cls.sender_instances or
                    not isinstance(cls.sender_instances[sender_name],
                        subclass)):
                    cls.sender_instances[sender_name] = subclass()
                return cls.sender_instances[sender_name]

    def _lookup_email_address(self, project_id):
        return [x.email for x in
                KeystoneClientSingleton.get_client().tenants.get(
                    project_id).list_users()]

    def add(self, **kwargs):
        notification = {x: kwargs[x] for x in self.params}
        notification['email'] = self._lookup_email_address(
            notification['project_id'])
        self.notifications.append(notification)

    def get_notifications(self):
        return [
            (self.subject,
             get_template(self.template).render(Context(notification)),
             self.from_email,
             notification['email'])
            for notification in self.notifications]


class LowBalanceNotifications(Notifications):
    name = 'low_balance'
    params = Notifications.params + ['passed_limit', 'current_balance']
    template = 'notifications/low_balance.txt'
    subject = 'Your balance is low'
