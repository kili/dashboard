from django import test
from resource_pricing.calculators import base
from resource_pricing import models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr_usd = models.Currency.objects.create(iso="USD")
        self.other_curr = models.Currency.objects.create(iso="OTHERCURR")
        self.resource1 = models.Resource.objects.create(
            resource_type_id=0, description="resource1")
        self.price = models.Price.objects.create(currency=self.curr_usd,
                                                 resource=self.resource1,
                                                 price=90)
        base.CalculatorBase.type_name = "testtype1"
        self.cb = base.CalculatorBase()
        base.VolumeAndInstancePriceCalculatorBase.resource_type_relation = \
            "resource__volumetype__os_type_id"
        base.VolumeAndInstancePriceCalculatorBase.type_name = "testtype1"
        self.vaipcb = base.VolumeAndInstancePriceCalculatorBase()

    def test_type_is_configured(self):
        self.cb.type_name = "testtype1"
        self.assertEqual(self.cb._type_is_configured(), True)
        self.cb.type_name = "nope"
        self.assertEqual(self.cb._type_is_configured(), False)

    def test_validate_params(self):
        self.cb.required_params = ["param1", "param2"]
        self.cb.optional_params = ["param3", "param4"]
        with self.assertRaises(Exception) as exception_context:
            self.cb._validate_params({"param1": 1})
        self.assertEqual(
            str(exception_context.exception),
            "the required parameter param2 is missing")
        self.assertEqual(self.cb._validate_params({
            "param1": 1,
            "param2": 2}), None)
        self.assertEqual(self.cb._validate_params({
            "param1": 1,
            "param2": 2,
            "param3": 3,
            "param4": 4}), None)
        with self.assertRaises(Exception) as exception_context:
            self.cb._validate_params({
                "param1": 1,
                "param2": 2,
                "param3": 3,
                "param5": 5})
        self.assertEqual(
            str(exception_context.exception),
            "the given parameter param5 is unknown")

    def test_init(self):
        base.CalculatorBase.type_name = "idontexist"
        with self.assertRaises(Exception) as exception_context:
            base.CalculatorBase()
        self.assertEqual(str(exception_context.exception),
                         "the type idontexist is not configured")

    def test_could_not_get_price_exception(self):
        with self.assertRaises(Exception) as exception_context:
            self.vaipcb._get_unit_price(self.resource1.id, "OTHERCURR")
        self.assertEqual(str(exception_context.exception),
                         "Could not get price of id 1 in currency "
                         "OTHERCURR")
