from openstack_dashboard.test import helpers as test  # noqa
from django.conf import settings


class PaymentsTests(test.TestCase):
    # Unit tests for payments.

    def test_me(self):
        self.assertTrue(1 + 1 == 2)
