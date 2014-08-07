import decimal
from django import test
#from billing_app import models as ba_models
from resource_pricing.calculators import calculators
from resource_pricing.calculators import models as calc_models
from resource_pricing import models as rp_models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr = rp_models.Currency.objects.create(iso='USD')
        self.ipc = calculators.CalculatorBase.get_price_calculator('instance')

    def test_regular_instance_price(self):
        tests = [
            {'price': 5, 'hours': '15', 'result': '75', 'flav': 'flav1'},
            {'price': 1, 'hours': '5.3', 'result': '5.3', 'flav': 'flav2'},
            {'price': 5.2, 'hours': '5', 'result': '26', 'flav': 'flav3'},
            {'price': 5.4, 'hours': '0.1', 'result': '0.54', 'flav': 'flav4'}]
        for test in tests:
            resource = calc_models.InstanceType.objects.create(
                os_instance_type_id=test['flav'])
            rp_models.Price.objects.create(
                currency=self.curr,
                resource=resource,
                price=test['price'])
            self.assertTrue(self.ipc.price_from_stats({
                'id': u'1',
                'hours': decimal.Decimal(test['hours']),
                'flavor': test['flav'],
                'resources': [u'inst1', u'inst2'],
                'tenant_id': u'333'
            })['price'].compare(
                decimal.Decimal(test['result'])) ==
                decimal.Decimal('0.000'))

    def test_single_reservation_price(self):
        pass
