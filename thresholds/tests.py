import pickle
from django.core import mail
from django.utils import timezone
from openstack_dashboard.test import helpers as test
from accounting.transactions import UserTransactions
from novaclient.v1_1.servers import ServerManager
from novaclient.v1_1.servers import Server
from keystone_wrapper.client import KeystoneClient
from notifications.tests import get_stub_keystone_client
from notifications.notification_sender import Notifications
from thresholds.models import PassedThreshold
from thresholds.models import Threshold
from thresholds.event_handlers import StopProjectInstancesThresholdAction
from thresholds.balance_thresholds import ActionQueueProcessor

my_tenant_id = 1
other_tenant_id = 2
instance_list = [
    Server(None, {'name': 'ser1', 'tenant_id': my_tenant_id}),
    Server(None, {'name': 'ser2', 'tenant_id': other_tenant_id}),
    Server(None, {'name': 'ser3', 'tenant_id': my_tenant_id}),
    Server(None, {'name': 'ser4', 'tenant_id': other_tenant_id})]


class ThresholdTests(test.TestCase):

    def setUp(self):
        super(ThresholdTests, self).setUp()
        self.real_now = timezone.now()

    @test.create_stubs({ServerManager: ('list',),
                        StopProjectInstancesThresholdAction: (
                            '_get_due_datetime',),
                        instance_list[0]: ('stop',),
                        instance_list[2]: ('stop',)})
    def test_instance_stopper(self):
        Threshold.objects.create(
            balance=-50,
            actions=pickle.dumps(['stop_project_instances']),
            up=False,
            down=True)
        ServerManager.list().AndReturn(instance_list)
        instance_list[0].stop()
        instance_list[2].stop()
        StopProjectInstancesThresholdAction._get_due_datetime().AndReturn(
            timezone.now())
        self.mox.ReplayAll()
        UserTransactions().consume_user_money(1, 60, 'some consumption')
        ActionQueueProcessor.process()

    @test.create_stubs({ServerManager: ('list',),
                        timezone: ('now',),
                        instance_list[0]: ('stop',),
                        instance_list[2]: ('stop',)})
    def test_action_queue_delay(self):
        Threshold.objects.create(
            balance=-50,
            actions=pickle.dumps(['stop_project_instances']),
            up=False,
            down=True)
        ServerManager.list().AndReturn(instance_list)
        instance_list[0].stop()
        instance_list[2].stop()
        timezone.now().AndReturn(self.real_now)  # called by user transaction
        timezone.now().AndReturn(self.real_now)  # called by user transaction
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=2 * 24 * 60 * 60))
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=3 * 24 * 60 * 60))
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=5 * 24 * 60 * 60))
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=6 * 24 * 60 * 60))
        self.mox.ReplayAll()
        UserTransactions().consume_user_money(1, 60, 'some consumption')
        ActionQueueProcessor.process()
        ActionQueueProcessor.process()
        ActionQueueProcessor.process()
        ActionQueueProcessor.process()

    # this test simulates a whole scenario:
    # create two thresholds, one at 0 and one at -50:
    # - the one at 0 sends a notification to the project's users
    # - the one at -50 sends a notification at the time of passing
    #    and also stops the instances of the project after 4 days have passed
    @test.create_stubs({ServerManager: ('list',),
                        KeystoneClient: ('get_client',),
                        timezone: ('now',),
                        instance_list[0]: ('stop',),
                        instance_list[2]: ('stop',)})
    def test_notification_sender_and_instance_stopper_combination(self):
        Notifications.delete_all_notifications()
        Threshold.objects.create(
            balance=0,
            actions=pickle.dumps(['send_notification']),
            up=False,
            down=True)
        Threshold.objects.create(
            balance=-50,
            actions=pickle.dumps(['send_notification',
                                  'stop_project_instances']),
            up=False,
            down=True)
        KeystoneClient.get_client().AndReturn(
            get_stub_keystone_client(3))
        KeystoneClient.get_client().AndReturn(
            get_stub_keystone_client(3))
        ServerManager.list().AndReturn(instance_list)
        instance_list[0].stop()
        instance_list[2].stop()
        timezone.now().AndReturn(self.real_now)  # called by user transaction
        timezone.now().AndReturn(self.real_now)  # called by user transaction
        timezone.now().AndReturn(self.real_now)  # called by user transaction
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=2 * 24 * 60 * 60))
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=3 * 24 * 60 * 60))
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=5 * 24 * 60 * 60))
        timezone.now().AndReturn(
            self.real_now + timezone.timedelta(seconds=6 * 24 * 60 * 60))
        self.mox.ReplayAll()
        ut = UserTransactions()
        ut.receive_user_payment(1, 'STRIPE', 6, 'user paid something')
        ut.consume_user_money(1, 100, 'lot of consumption')
        Notifications.send_all_notifications()
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(PassedThreshold.objects.count(), 2)
        ActionQueueProcessor.process()
        ActionQueueProcessor.process()
        self.assertEqual(len(instance_list[0].stop._expected_calls_queue), 1)
        self.assertEqual(len(instance_list[2].stop._expected_calls_queue), 1)
        ActionQueueProcessor.process()
        self.assertEqual(len(instance_list[0].stop._expected_calls_queue), 0)
        self.assertEqual(len(instance_list[2].stop._expected_calls_queue), 0)
        ActionQueueProcessor.process()
