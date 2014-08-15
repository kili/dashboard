from django.core import mail
from openstack_dashboard.test import helpers as test
from notifications.notification_sender import Notifications
from notifications.notification_sender import LowBalanceNotifications
from keystone_wrapper.client import KeystoneClientSingleton


class StubObject(object):
    pass


class SimpleTest(test.TestCase):

    @test.create_stubs({KeystoneClientSingleton: ('get_client',)})
    def test_send_low_balance_notification(self):
        number_recipients = 5

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
        KeystoneClientSingleton.get_client().AndReturn(stub_client)
        self.mox.ReplayAll()
        Notifications.get_notification_sender('low_balance').add(
            project_id=1, passed_limit=5, current_balance=4)
        Notifications.send_all_notifications()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         LowBalanceNotifications.subject)
        self.assertEqual(mail.outbox[0].from_email,
                         LowBalanceNotifications.from_email)
        self.assertEqual(len(mail.outbox[0].to),
                         number_recipients)
