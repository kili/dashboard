from django import test
from resource_pricing.calculators import calculators
from resource_pricing import models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr_usd = models.Currency.objects.create(iso="USD")
        self.other_curr = models.Currency.objects.create(iso="OTHERCURR")
        self.resource1 = models.Resource.objects.create(resource_type_id=0)
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource1,
                                                 price=90)
        self.ipc = calculators.InstancePriceCalculator()
        self.vpc = calculators.VolumePriceCalculator()

    def test_validate_params(self):
        with self.assertRaises(Exception) as exception_context:
            self.ipc._validate_params({'hours': 1, 'res_string': 'abc'})
        self.assertEqual(
            str(exception_context.exception),
            "the required parameter flavor is missing")
        with self.assertRaises(Exception) as exception_context:
            self.vpc._validate_params(
                {'hours': 1, 'type': 'a', 'res_string': 'abc'})
        self.assertEqual(
            str(exception_context.exception),
            "the required parameter gb_size is missing")
        with self.assertRaises(Exception) as exception_context:
            self.ipc._validate_params({
                'hours': 1,
                'flavor': 2,
                'res_string': 3,
                'other_param': 4})
        self.assertEqual(
            str(exception_context.exception),
            "the given parameter other_param is unknown")

    def test_init(self):
        self.ipc.type_name = 'idontexist'
        with self.assertRaises(Exception) as exception_context:
            self.ipc.__init__()
        self.assertEqual(str(exception_context.exception),
                         "the type idontexist is not configured")
