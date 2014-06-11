from django.conf import settings
from openstack_dashboard.test import helpers as test  # noqa


class PaymentsTests(test.TestCase):
    # Unit tests for payments.

    def test_environment_sanity(self):
        # make sure our test environment is realy in TEST MODE

        self.assertTrue(settings.MERCHANT_TEST_MODE)
        self.assertTrue(
            "test" in
            settings.MERCHANT_SETTINGS['stripe']['API_KEY'])
        self.assertTrue(
            "test" in
            settings.MERCHANT_SETTINGS['stripe']['PUBLISHABLE_KEY'])

    # integration tests

    def test_add_card(self):
        pass

    def test_add_invalid_card(self):
        pass
