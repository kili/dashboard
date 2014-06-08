import decimal
from django import test
from resource_pricing.calculators.volume import calculator
from resource_pricing.calculators.volume import models as volume_models
from resource_pricing import models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr_usd = models.Currency.objects.create(iso='USD')
        self.resource1 = models.Resource.objects.create(
            resource_type_id=0, description='my test type1')
        self.resource2 = models.Resource.objects.create(
            resource_type_id=0, description='my test type2')
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource1,
                                                 price=0.01)
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource2,
                                                 price=9.95)
        self.type1 = volume_models.VolumeType.objects.create(
            os_type_id='type1', resource=self.resource1)
        self.type2 = volume_models.VolumeType.objects.create(
            os_type_id='type2', resource=self.resource2)
        calculator.VolumePriceCalculator.type_name = 'testtype1'
        self.vpc = calculator.VolumePriceCalculator()

    def test_final_price_calculation(self):
        self.assertEqual(
            self.vpc.get_price({'type': 'type1', 'hours': 3, 'gb_size': 100}).
            compare_total(decimal.Decimal('3.00')),
            decimal.Decimal(0))
        self.assertEqual(
            self.vpc.get_price({'type': 'type1', 'hours': 3.5, 'gb_size': 50}).
            compare_total(decimal.Decimal('1.750')),
            decimal.Decimal(0))
        self.assertEqual(
            self.vpc.get_price({'type': 'type2', 'hours': 3, 'gb_size': 2})
            .compare(decimal.Decimal('59.70')),
            decimal.Decimal(0))
        with self.assertRaises(Exception) as exception_context:
            self.vpc.get_price({'type': 'type1', 'hours': -1, 'gb_size': 1})
        self.assertEqual(str(exception_context.exception),
                         'the consumed hours cannot be less than 0')
        with self.assertRaises(Exception) as exception_context:
            self.vpc.get_price({'abc': 'type1', 'hours': 3})
        self.assertEqual(str(exception_context.exception),
                         'the required parameter gb_size is missing')
        with self.assertRaises(Exception) as exception_context:
            self.vpc.get_price({'gb_size': 'type1', 'hour': 3})
        self.assertEqual(str(exception_context.exception),
                         'the required parameter hours is missing')
        with self.assertRaises(Exception) as exception_context:
            self.vpc.get_price({'type': 'type1', 'hours': 1, 'gb_size': 0.5})
        self.assertEqual(str(exception_context.exception),
                         'the given gb_size cannot be less than 1')
