import decimal
from django import test
from resource_pricing.calculators.volume import calculator
from resource_pricing.calculators.volume import models as volume_models
from resource_pricing import models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr_usd = models.Currency.objects.create(iso='USD')
        self.resource1 = models.Resource.objects.create(
            resource_type_id=1, description='my test type1')
        self.resource2 = models.Resource.objects.create(
            resource_type_id=1, description='my test type2')
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource1,
                                                 price=0.01)
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource2,
                                                 price=9.95)
        self.type1 = volume_models.VolumeType.objects.create(
            os_type_id='volume:type1', resource=self.resource1)
        self.type2 = volume_models.VolumeType.objects.create(
            os_type_id='volume:type2', resource=self.resource2)
        calculator.PriceCalculator.type_name = 'testtype1'
        self.vpc = calculator.PriceCalculator()

    def test_final_price_calculation(self):
        self.assertEqual(
            self.vpc.price_from_raw_stats(
                [{'count': 18},
                 {'metadata': {
                     'gb_size': 100,
                     'type': 'type1',
                     'display_name': 'type1'}}])['price'].compare(
                         decimal.Decimal(3)), decimal.Decimal(0))
        self.assertEqual(
            self.vpc.price_from_raw_stats(
                [{'count': 21},
                 {'metadata': {
                     'gb_size': 50,
                     'type': 'type1',
                     'display_name': 'type1'}}])['price'].compare(
                         decimal.Decimal(1.750)), decimal.Decimal(0))
        self.assertEqual(
            self.vpc.price_from_raw_stats(
                [{'count': 18},
                 {'metadata': {
                     'gb_size': 2,
                     'type': 'type2',
                     'display_name': 'type2'}}])['price'].compare(
                         decimal.Decimal('59.70')), decimal.Decimal(0))
        with self.assertRaises(Exception) as exception_context:
            self.vpc.price_from_raw_stats(
                [{'count': -1},
                 {'metadata': {
                     'gb_size': 1,
                     'type': 'type1',
                     'display_name': 'type1'}}])
        self.assertEqual(str(exception_context.exception),
                         'the consumed hours cannot be less than 0')
        with self.assertRaises(Exception) as exception_context:
            self.vpc._validate_params({'abc': 'type1',
                                       'hours': 3,
                                       'res_string': 'abc'})
        self.assertEqual(str(exception_context.exception),
                         'the required parameter gb_size is missing')
        with self.assertRaises(Exception) as exception_context:
            self.vpc._validate_params({'type': 'bla',
                                       'gb_size': 10,
                                       'hour': 3,
                                       'res_string': 'abc'})
        self.assertEqual(str(exception_context.exception),
                         'the required parameter hours is missing')
        with self.assertRaises(Exception) as exception_context:
            self.vpc._validate_params({'type': 'bla',
                                       'gb_size': 10,
                                       'hours': 3,
                                       'resstring': 'abc'})
        self.assertEqual(str(exception_context.exception),
                         'the required parameter res_string is missing')
        with self.assertRaises(Exception) as exception_context:
            self.vpc._validate_params({'type': 'type1',
                                       'hours': 1,
                                       'gb_size': 0.5,
                                       'res_string': 'abc'})
        self.assertEqual(str(exception_context.exception),
                         'the given gb_size cannot be less than 1')