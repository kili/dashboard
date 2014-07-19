from django import test
from resource_pricing.calculators import calculators
from resource_pricing import models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr_usd = models.Currency.objects.create(iso="USD")
        self.other_curr = models.Currency.objects.create(iso="OTHERCURR")
        self.ipc = calculators.InstancePriceCalculator()
        self.vpc = calculators.VolumePriceCalculator()

    def test_init(self):
        self.ipc.meter_name = 'idontexist'
        with self.assertRaises(Exception) as exception_context:
            self.ipc.__init__()
        self.assertEqual(str(exception_context.exception),
                         "the type idontexist is not configured")
