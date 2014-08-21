import pickle
from django.core import mail
from openstack_dashboard.test import helpers as test
from thresholds.models import Threshold
from thresholds.models import PassedThreshold
from notifications.notification_sender import Notifications
from notifications.notification_sender import LowBalanceNotificationSender
from keystone_wrapper.client import KeystoneClient
from accounting.transactions import UserTransactions


def get_stub_keystone_client(number_recipients):

    class StubObject(object):
        pass

    def return_tenant(arg1):
        def return_user_list():
            def create_user_object(num):
                ob = StubObject()
                setattr(ob, 'email', 'email{0}'.format(num))
                return ob
            return [create_user_object(i)
                    for i in range(0, number_recipients)]
        stub_tenant = StubObject()
        setattr(stub_tenant, 'list_users', return_user_list)
        return stub_tenant

    stub_tenants = StubObject()
    setattr(stub_tenants, 'get', return_tenant)
    stub_client = StubObject()
    setattr(stub_client, 'tenants', stub_tenants)
    return stub_client


class NotificationsTests(test.TestCase):

    @test.create_stubs({KeystoneClient: ('get_client',)})
    def test_notification_sending(self):
        Notifications.sender_instances = {}
        number_recipients = 5
        KeystoneClient.get_client().AndReturn(
            get_stub_keystone_client(number_recipients))
        self.mox.ReplayAll()
        Notifications.get_notification_sender('low_balance').add(
            project_id=1,
            passed_limit=5,
            current_balance=4)
        Notifications.send_all_notifications()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         LowBalanceNotificationSender.subject)
        self.assertEqual(mail.outbox[0].from_email,
                         LowBalanceNotificationSender.from_email)
        self.assertEqual(len(mail.outbox[0].to),
                         number_recipients)

    @test.create_stubs({KeystoneClient: ('get_client',)})
    def test_low_balance_notification(self):
        Notifications.sender_instances = {}
        threshold = Threshold.objects.create(
            balance=5,
            actions=pickle.dumps(['send_notification']),
            up=False,
            down=True)
        number_recipients = 1
        KeystoneClient.get_client().AndReturn(
            get_stub_keystone_client(number_recipients))
        self.mox.ReplayAll()
        ut = UserTransactions()
        ut.receive_user_payment(1, 'STRIPE', 6, 'tester paid')
        ut.consume_user_money(1, 4, 'some consumption')
        Notifications.send_all_notifications()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         LowBalanceNotificationSender.subject)
        self.assertEqual(mail.outbox[0].from_email,
                         LowBalanceNotificationSender.from_email)
        self.assertEqual(len(mail.outbox[0].to),
                         number_recipients)
        self.assertEqual(PassedThreshold.objects.count(), 1)
        self.assertEqual(PassedThreshold.objects.all()[0].threshold,
                         threshold)
