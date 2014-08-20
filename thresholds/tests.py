import pickle
from django.utils import timezone
from openstack_dashboard.test import helpers as test
from thresholds.models import Threshold
from thresholds.models import PassedThreshold
from accounting.transactions import UserTransactions
from thresholds.event_handlers import StopProjectInstances
from thresholds.balance_thresholds import ActionQueueProcessor


class SimpleTest(test.TestCase):

    def setUp(self):
        @classmethod
        def stub_get_due_datetime(cls):
            return timezone.now()
        self.stub_get_due_datetime = stub_get_due_datetime

    @test.create_stubs({api.nova: ('server_list',)})
    def test_low_balance_notification(self):
        threshold = Threshold.objects.create(
            balance=-50,
            actions=pickle.dumps(['stop_project_instances']),
            up=False,
            down=True)
        StopProjectInstances._get_due_datetime = self.stub_get_due_datetime
        UserTransactions().consume_user_money(1, 60, 'some consumption')
        ActionQueueProcessor.process()
