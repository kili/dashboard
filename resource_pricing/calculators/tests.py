from django import test
from resource_pricing.calculators import calculators
from resource_pricing import models


class SimpleTest(test.TestCase):

    def setUp(self):
        self.curr_usd = models.Currency.objects.create(iso="USD")
        self.other_curr = models.Currency.objects.create(iso="OTHERCURR")
        self.ipc = calculators.InstancePriceCalculator()
        self.vpc = calculators.VolumePriceCalculator()
