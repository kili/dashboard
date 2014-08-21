import pickle
from django.utils import timezone
from openstack_dashboard.test import helpers as test
from accounting.transactions import UserTransactions
from novaclient.v1_1.servers import ServerManager
from novaclient.v1_1.servers import Server
from thresholds.models import Threshold
from thresholds.event_handlers import StopProjectInstances
from thresholds.balance_thresholds import ActionQueueProcessor

my_tenant_id = 1
other_tenant_id = 2
instance_list = [
    Server(None, {'name': 'ser1', 'tenant_id': my_tenant_id}),
    Server(None, {'name': 'ser2', 'tenant_id': other_tenant_id}),
    Server(None, {'name': 'ser3', 'tenant_id': my_tenant_id})]


class ThresholdTests(test.TestCase):

    def setUp(self):
        super(ThresholdTests, self).setUp()
        self.real_now = timezone.now()

    @test.create_stubs({ServerManager: ('list',),
                        StopProjectInstances: ('_get_due_datetime',),
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
        StopProjectInstances._get_due_datetime().AndReturn(timezone.now())
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
