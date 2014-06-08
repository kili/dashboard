from django import test
from resource_pricing import types


class SimpleTest(test.TestCase):

    def setUp(self):
        self.resource_types = types.ResourceTypes()

    def test_getting_price_calculator(self):
        self.assertEqual(
            self.resource_types.get_price_calculator('testtype1'),
            'testcalculator1')
        with self.assertRaises(Exception) as exception_context:
            self.resource_types.get_price_calculator('idontexist')
        self.assertEqual(
            str(exception_context.exception),
            'the price calculator for type idontexist is not configured')
