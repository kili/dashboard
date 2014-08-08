import decimal
import datetime
from django import test
from django.utils import timezone
from billing_app import models as ba_models
from resource_pricing.calculators import calculators
from resource_pricing.calculators import models as calc_models
from resource_pricing import models as rp_models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.ipc = calculators.CalculatorBase.get_price_calculator('instance')
        curr = rp_models.Currency.objects.create(iso='USD')
        prices = [
            {'flav': 'flav1', 'price': 5},
            {'flav': 'flav2', 'price': 1},
            {'flav': 'flav3', 'price': 5.2},
            {'flav': 'flav4', 'price': 5.4}]
        self.prices = []
        for price in prices:
            self.prices.append(
                rp_models.Price.objects.create(
                    currency=curr,
                    resource=calc_models.InstanceType.objects.create(
                        os_instance_type_id=price['flav']),
                    price=decimal.Decimal(price['price'])))

        self.reservations = []
        reservations = [
            {'type': u'1',
             'hourly_price': '1.2',
             'upfront_price': '5.5'},
            {'type': u'2',
             'hourly_price': '8.0',
             'upfront_price': '50'},
            {'type': u'1',
             'hourly_price': '2.2',
             'upfront_price': '10'}]
        for reservation in reservations:
            self.reservations.append(
                ba_models.PrePaidReservation.objects.create(
                    instance_type=reservation['type'],
                    hourly_price=decimal.Decimal(
                        reservation['hourly_price']),
                    upfront_price=decimal.Decimal(
                        reservation['upfront_price']),
                    length=365,
                    available=True))

    def test_regular_instance_price_calculation(self):
        testcases = [
            {'price': 0, 'hours': '15', 'result': '75'},
            {'price': 1, 'hours': '5.3', 'result': '5.3'},
            {'price': 2, 'hours': '5', 'result': '26'},
            {'price': 3, 'hours': '0.1', 'result': '0.54'}]

        for test in testcases:
            self.assertTrue(self.ipc.price_from_stats({
                'id': u'1',
                'hours': decimal.Decimal(test['hours']),
                'flavor': self.prices[
                    test['price']].resource.os_instance_type_id,
                'resources': [u'inst1', u'inst2'],
                'tenant_id': u'333'
            })['price'].compare(
                decimal.Decimal(test['result'])) ==
                decimal.Decimal('0.000'))

    def test_single_reservation_price_calculation1(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('20'),
            'flavor': 'flav1',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('24.0')) ==
            decimal.Decimal('0.000'))

    def test_single_reservation_price_calculation2(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('30'),
            'flavor': 'flav3',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('60.0')) ==
            decimal.Decimal('0.000'))

    def test_single_reservation_price_calculation3(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() + datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=2),
            prepaid_reservation=self.reservations[0])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('30'),
            'flavor': 'flav3',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('156.0')) ==
            decimal.Decimal('0.000'))

    def test_multi_reservation_price_calculation1(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[2])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('30'),
            'flavor': 'flav1',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('42')) ==
            decimal.Decimal('0.000'))

    def test_multi_reservation_price_calculation2(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[2])
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('30'),
            'flavor': 'flav1',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('42')) ==
            decimal.Decimal('0.000'))

    def test_multi_reservation_price_calculation3(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[2])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('50'),
            'flavor': 'flav1',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('91.6')) ==
            decimal.Decimal('0.000'))

    def test_multi_reservation_price_calculation4(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[2])
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('50'),
            'flavor': 'flav1',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('62.0')) ==
            decimal.Decimal('0.000'))

    def test_multi_reservation_price_calculation5(self):
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() - datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1),
            prepaid_reservation=self.reservations[0])
        ba_models.AssignedReservation.objects.create(
            tenant_id='333',
            start=timezone.now() + datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=2),
            prepaid_reservation=self.reservations[2])

        self.assertTrue(self.ipc.price_from_stats({
            'id': u'1',
            'hours': decimal.Decimal('50'),
            'flavor': 'flav1',
            'resources': [u'inst1', u'inst2'],
            'tenant_id': u'333'
        })['price'].compare(
            decimal.Decimal('67.6')) ==
            decimal.Decimal('0.000'))
