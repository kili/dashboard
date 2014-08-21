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
        @classmethod
        def stub_get_due_datetime(cls):
            return timezone.now()

        self.stub_get_due_datetime = stub_get_due_datetime
        super(ThresholdTests, self).setUp()

    @test.create_stubs({ServerManager: ('list',),
                        instance_list[0]: ('stop',),
                        instance_list[2]: ('stop',)})
    def test_low_balance_notification(self):
        Threshold.objects.create(
            balance=-50,
            actions=pickle.dumps(['stop_project_instances']),
            up=False,
            down=True)
        ServerManager.list().AndReturn(instance_list)
        instance_list[0].stop()
        instance_list[2].stop()
        self.mox.ReplayAll()
        StopProjectInstances._get_due_datetime = self.stub_get_due_datetime
        UserTransactions().consume_user_money(1, 60, 'some consumption')
        ActionQueueProcessor.process()
        self.mox.VerifyAll()
