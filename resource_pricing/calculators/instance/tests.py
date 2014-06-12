import decimal
from django import test
from resource_pricing.calculators.instance import calculator
from resource_pricing.calculators.instance import models as instance_models
from resource_pricing import models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr_usd = models.Currency.objects.create(iso='USD')
        self.resource1 = models.Resource.objects.create(
            resource_type_id=0, description='my test flavor1')
        self.resource2 = models.Resource.objects.create(
            resource_type_id=0, description='my test flavor2')
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource1,
                                                 price=90)
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource2,
                                                 price=10)
        self.flavor1 = instance_models.Flavor.objects.create(
            os_flavor_id='flavor1', resource=self.resource1)
        self.flavor2 = instance_models.Flavor.objects.create(
            os_flavor_id='flavor2', resource=self.resource2)
        calculator.PriceCalculator.type_name = 'testtype1'
        self.ipc = calculator.PriceCalculator()

    def test_final_price_calculation(self):
        self.assertEqual(
            self.ipc.price_from_raw_stats('flavor1', {'count': 18}).compare(
                decimal.Decimal(270)), decimal.Decimal(0))
        self.assertEqual(
            self.ipc.price_from_raw_stats('flavor1', {'count': 9}).compare(
                decimal.Decimal(135)), decimal.Decimal(0))
        self.assertEqual(
            self.ipc.price_from_raw_stats('flavor2', {'count': 18}).compare(
                decimal.Decimal(30)), decimal.Decimal(0))
        with self.assertRaises(Exception) as exception_context:
            self.ipc.price_from_raw_stats('flavor1', {'count': -1})
        self.assertEqual(str(exception_context.exception),
                         'the consumed hours cannot be less than 0')
        with self.assertRaises(Exception) as exception_context:
            self.ipc._validate_params({'abc': 'flavor1', 'hours': 3})
        self.assertEqual(str(exception_context.exception),
                         'the required parameter flavor is missing')
